from typing import *

import asyncio

from datetime import datetime

import discord
from discord.ext import commands
from discord import app_commands, Interaction
from discord import VoiceClient, VoiceChannel, StageChannel, VoiceState
from discord import Guild

from .playerbase import PlayerBase, PlayerBaseCog
from .playlist import Song, Playlist

class PlayingSession(PlayerBase):
    def __init__(self, text_channel: discord.TextChannel):
        self.text_channel = text_channel
        self.guild = text_channel.guild
        self.queue = Playlist(self.guild.id)
        self.voice_client = self.guild.voice_client
        self.task = None
    
    def using(self):
        if not isinstance(self.voice_client, VoiceClient):
            return False
        return self.voice_client.is_playing() or self.voice_client.is_paused()

    def running(self):
        return isinstance(self.task, asyncio.Task) and not self.task.done()

    async def start_session(self):
        if self.running():
            return
        loop = asyncio.get_event_loop()
        self.task = loop.create_task(self.run())

    async def run(self):
        try:
            while not self.queue.empty():
                if self.queue[0].expired:
                    await self.queue[0].get_full_info()
                await self._play_source(self.voice_client.channel, 
                        discord.FFmpegPCMAudio(self.queue[0].url, **{
                            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 10',
                        }))
                # {
                #     'options': f'-vn -ss {timestamp}',
                #     'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 10',
                # }
                # await self.text_channel.send(embed=await self.queue[0].render())
                await self.wait()
                self.queue.delete_song(0)
        except Exception as e:
            raise e
            raise Exception('idk')

    async def wait(self):
        try:
            while self.using():
                await asyncio.sleep(3.0)
        except:
            self.voice_client.stop()

    async def add_to_queue(self, url: str, idx: int = -1):
        await self.queue.add_songs(url)

    async def _sort(self):
        await self.queue.sort()

class Player(PlayerBase):
    def __init__(self):
        # self.playlist: Mapping[int, Playlist] = dict()
        # self.playlist = Playlist()
        self.playing_session: Mapping[int, PlayingSession] = dict()

    def ensure_session_exist(self):
        pass

    async def _play(self, text_channel: discord.TextChannel, url: str):
        guild_id = text_channel.guild.id
        if self.playing_session.get(guild_id) is None:
            self.playing_session[guild_id] = PlayingSession(text_channel)
        
        await self.playing_session[guild_id].add_to_queue(url)

        if not self.playing_session[guild_id].running():
            await self.playing_session[guild_id].start_session()

    async def _sort(self, guild: discord.Guild):
        await self.playing_session[guild.id]._sort()

class PlayerCog(Player, PlayerBaseCog, commands.Cog):
    def __init__(self):
        super().__init__()

    @app_commands.command(name="play", description="撥放音樂或清單")
    async def play(self, interaction: Interaction, url: str):
        if interaction.user.voice is None:
            await self.sent_embed(interaction,0xde1f1f,"無法找到語音頻道!")
            return
        await self._join(interaction.user.voice.channel)
        await interaction.response.defer(thinking=True, ephemeral=True)
        await self._play(interaction.channel, url)
        
        await interaction.edit_original_response(content=url)
        embed = discord.Embed(
            title="已加入一首音樂!",
            color=0x23fa4a,
            timestamp=datetime.now(),
            url = url
        )
        await interaction.channel.send(embed=embed)
    
    @app_commands.command(name="sort", description="將現有清單最佳化排序")
    async def sort(self, interaction: Interaction):
        await interaction.response.defer(thinking=True)
        await self._sort(interaction.guild)
        embed = discord.Embed(
            title="已排序完成!",
            color=0x23fa4a,
            timestamp=datetime.now(),
        )
        await interaction.edit_original_response(embed=embed)

    @app_commands.command(name="song", description="hello")
    async def song_info(self, interaction: Interaction, idx: int):
        if not self.playing_session[interaction.guild.id].running():
            return
        if idx >= len(self.playing_session[interaction.guild.id].queue):
            return
        
        embed = await self.playing_session[interaction.guild.id].queue[idx].render()
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="nowplaying", description="hello")
    async def nowplaying(self, interaction: Interaction):
        if not self.playing_session[interaction.guild.id].running():
            return
        
        embed = await self.playing_session[interaction.guild.id].queue.nowplaying.render()
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="queue", description="hello")
    async def queue_info(self, interaction: Interaction):
        if not self.playing_session[interaction.guild.id].running():
            return
        
        embed = await self.playing_session[interaction.guild.id].queue.render()
        await interaction.response.send_message(embed=embed)
