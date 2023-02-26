from typing import *

import asyncio

import discord
from discord.ext import commands
from discord import app_commands, Interaction
from discord import VoiceClient, VoiceChannel, StageChannel, VoiceState
from discord import Guild

from .playerbase import PlayerBase, PlayerBaseCog
from .playlist import Song, PlaylistBase, Playlist

class PlayingSession(PlayerBase):
    def __init__(self, text_channel: discord.TextChannel):
        self.text_channel = text_channel
        self.guild = text_channel.guild
        self.queue = PlaylistBase(self.guild.id)
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
                await self._play_source(self.voice_client.channel, 
                        discord.FFmpegPCMAudio(self.queue[0].url, **{
                            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 10',
                        }))
                # {
                #     'options': f'-vn -ss {timestamp}',
                #     'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 10',
                # }
                await self.text_channel.send("success to play this song")
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
        self.queue.add_songs(url)

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


class PlayerCog(Player, PlayerBaseCog, commands.Cog):
    def __init__(self):
        super().__init__()

    @app_commands.command(name="play", description="Play the song or playlist you want")
    async def play(self, interaction: Interaction, qstring: str):
        if not await self._connectable_channel(interaction):
            return
        # await self.join(interaction)
        await interaction.response.defer(thinking=True)
        await self._play(interaction.channel, qstring)
        await interaction.edit_original_response(content="Succeed to play the music")
