from typing import *

import time
from urllib.parse import urlparse
from urllib.parse import parse_qs

from .downloader import YoutubeDownloader

from intergrated import intergrated_tools

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
    
    def __init__(self, id):
        self.id = id

    async def get_full_info(self):
        """
        Retrieve the full song info
        """
        info = await YoutubeDownloader.get_info(self.id)
        
        self._title = info["title"]
        self._url = info["url"]
        self._weburl = info["weburl"]
        
        parsed_url = urlparse(self._url)
        self._expire_time = float(parse_qs(parsed_url.query)['expire'][0])

    def render(self) -> Embed:
        embed = Embed(
            title="Now playing",
            description="The infomation is below",
            colour=Colour.green(),
            url=self.weburl
        )
        embed.add_field(
            name="Title",
            value=self.title,
            inline=False
        )
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

    def empty(self):
        return len(self.playlist) == 0
    
    async def add_songs(self, url: str):
        ids = await YoutubeDownloader.get_ids(url)

        for id in ids:
            self.playlist.append(Song(id))

    def delete_song(self, idx):
        self.playlist.pop(idx)

    async def sort(self):
        scores = []

        for song in self.playlist:
            if song.expired:
                await song.get_full_info()

            intergrated_tools.class_and_score()
