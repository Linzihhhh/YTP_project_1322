from typing import *

import os
import subprocess

class YoutubeDownloader:

    @classmethod
    def get_ids(self, url: str) -> list:
        try:
            ids = subprocess.run(
                f'yt-dlp --ignore-errors --get-id "{url}"', capture_output=True).stdout.decode().split('\n')
            ids.pop() # remove the last empty string
            return ids
        except Exception as e:
            print(e)
    
    @classmethod
    def get_info(self, id: str, *, path: str = None): 
        """
        Download info of a song by given youtube video id
        """

        try:
            weburl = f"https://www.youtube.com/watch?v={id}"
            path = path or os.getcwd()

            info = {
                "id": id,
                "weburl": weburl,
            }

            info["url"] = subprocess.run(
                f"yt-dlp --ignore-errors --get-url {weburl}", capture_output=True).stdout.decode()

            info["url"] = info["url"].split('\n')[1]
            
            info["title"] = subprocess.run(
                f"yt-dlp --ignore-errors --get-title {weburl}", capture_output=True).stdout.decode()
            
            return info
        except Exception as e:
            print(e)

