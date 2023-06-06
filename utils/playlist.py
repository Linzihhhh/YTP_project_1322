from typing import *

import time
import asyncio
from urllib.parse import urlparse
from urllib.parse import parse_qs

import functools

from .downloader import YoutubeDownloader
from .type import EmotionType

from .predictor import predictor

import discord
from discord import Colour, Embed

class Song:

    # __slots__ = (
    #     "id",
    #     "title",
    #     "weburl",
    #     "url",
    #     "expired_time"
    # )

    _expire_time = 0

    @property
    def expired(self) -> bool:
        return time.time() >= self._expire_time

    @property
    def title(self):
        return self._title

    @property
    def weburl(self):
        return self._weburl

    @property
    def url(self):
        return self._url
    
    @property
    def duration(self):
        return self._duration
    
    @property
    def uploader(self):
        return self._uploader
    
    @property
    def channel_url(self):
        return self._channel_url
    
    @property
    def thumbnail(self):
        return self._thumbnail
    
    def __init__(self, id):
        self.id = id

    async def get_full_info(self):
        """
        Retrieve the full song info
        """
        info = await YoutubeDownloader.get_info(self.id)
        
        self._title = info["title"]
        self._url = info["requested_formats"][-1]["url"]
        self._weburl = info["webpage_url"]
        self._duration = info["duration"]
        self._thumbnail = info["thumbnail"]
        self._uploader = info["uploader"]
        self._channel_url = info["channel_url"]

        parsed_url = urlparse(self._url)
        self._expire_time = float(parse_qs(parsed_url.query)['expire'][0])

    async def render(self) -> Embed:
        if self.expired:
            await self.get_full_info()
        
        embed = Embed(
            title= self.title,
            url = self.weburl,
            colour=Colour.green(),
            description=f"[{self.uploader}]({self.channel_url})"
        )
        embed.set_image(url=self.thumbnail)
        return embed

class Playlist:

    # __slots__ = tuple("playlist")
    
    def __init__(self, guild_id: int):
        self.guild_id = guild_id
        self.playlist: List[Song] = []

    def __getitem__(self, idx) -> Song:
        return self.playlist[idx]

    def load(self):
        pass

    def dump(self):
        pass

    def empty(self) -> bool:
        return len(self.playlist) == 0
    
    @property
    def nowplaying(self) -> Optional[Song]:
        if not self.empty():
            return self.playlist[0]
        return None

    async def render(self) -> Embed:
        if len(self.playlist) < 2:
            embed = Embed(
                title="待播清單",
                color = Colour.green(),
                description="無待播音樂"
            )
            return embed
        elif len(self.playlist) < 9:
            embed = Embed(
                title="待播清單",
                color = Colour.green()
            )
            for i, song in enumerate(self.playlist[1:], 1):
                if song.expired:
                    await song.get_full_info()
                
                embed.add_field(
                    name="",
                    value=f"{i}. "+f"[{song.title}]({song.weburl})",
                    inline=False
                )
            return embed
        else:
            embed = Embed(
                title="待播清單",
                color = Colour.green()
            )
            for i, song in enumerate(self.playlist[1:8], 1):
                if song.expired:
                    await song.get_full_info()
                
                embed.add_field(
                    name="",
                    value=f"{i}. "+f"[{song.title}]({song.weburl})",
                    inline=False
                )
            embed.add_field(
                name="",
                value="..."
            )
            return embed

    async def add_songs(self, url: str):
        ids = await YoutubeDownloader.get_ids(url)

        for id in ids:
            self.playlist.append(Song(id))

    def delete_song(self, idx):
        self.playlist.pop(idx)

    async def keep(self, *emotions: EmotionType):

        playlist = []
        
        for song in self.playlist[1:]:

            result = await predictor.predict(f"{song.id}")
            await asyncio.sleep(0.1)

            if EmotionType(result) in emotions:
                playlist.append(song)

        self.playlist[1:] = playlist

    