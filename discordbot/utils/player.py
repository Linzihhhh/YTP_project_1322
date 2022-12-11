from typing import *

import discord
from discord.ext import commands
from discord import app_commands, Interaction
from discord import VoiceClient, VoiceChannel, StageChannel, VoiceState
from discord import Guild

from .playerbase import PlayerBase, PlayerBaseCog
from .playlist import Song, PlaylistBase, Playlist

class Player(PlayerBase):
    def __init__(self):
        # self.playlist: Mapping[int, Playlist] = dict()
        self.playlist = PlaylistBase()

    async def _play(self, channel: VoiceChannel, url: str):
        self.playlist.add_songs(url)
        await self._play_source(channel, discord.FFmpegPCMAudio(self.playlist.playlist[0].url))
        self.playlist.playlist.pop(0)

class PlayerCog(Player, PlayerBaseCog, commands.Cog):
    def __init__(self):
        super().__init__()

    @app_commands.command(name="play", description="Play the song or playlist you want")
    async def play(self, interaction: Interaction, qstring: str):
        if not await self._connectable_channel(interaction):
            return
        await interaction.response.defer(thinking=True)
        await self._play(interaction.user.voice.channel, qstring)
        await interaction.edit_original_response(content="Succeed to play the music")
