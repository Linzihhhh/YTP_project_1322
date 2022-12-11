from typing import *

import time
from urllib.parse import urlparse
from urllib.parse import parse_qs

from .downloader import YoutubeDownloader

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
        if self.expired:
            self.get_full_info()
        return self._title

    @property
    def weburl(self):
        if self.expired:
            self.get_full_info()
        return self._weburl

    @property
    def url(self):
        if self.expired:
            self.get_full_info()
        return self._url
    
    def __init__(self, id):
        self.id = id

    def get_full_info(self):
        """
        Retrieve the full song info
        """
        info = YoutubeDownloader.get_info(self.id)
        
        self._title = info["title"]
        self._url = info["url"]
        self._weburl = info["weburl"]
        
        parsed_url = urlparse(self._url)
        self._expire_time = float(parse_qs(parsed_url.query)['expire'][0])


class PlaylistBase:

    # __slots__ = tuple("playlist")
    
    def __init__(self):
        self.playlist: List[Song] = []

    def load(self):
        pass

    def dump(self):
        pass

    def add_songs(self, url: str):
        ids = YoutubeDownloader.get_ids(url)

        for id in ids:
            self.playlist.append(Song(id))


class Playlist:
    ...