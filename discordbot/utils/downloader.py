from typing import *

import os
import subprocess
import asyncio

class YoutubeDownloader:

    @classmethod
    async def get_ids(self, url: str) -> list:
        try:
            process = await asyncio.create_subprocess_shell(
                    f'yt-dlp --ignore-errors --get-id "{url}"', 
                    stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
            stdout, stderr = await process.communicate()
            if stderr:
                raise Exception(stderr.decode())
            
            ids = stdout.decode().split('\n')
            ids.pop() # remove the last empty string
            return ids
        except Exception as e:
            print(e)
    
    @classmethod
    async def get_info(self, id: str, *, path: str = None): 
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

            process = await asyncio.create_subprocess_shell(
                    f"yt-dlp --ignore-errors --get-url {weburl}", 
                    stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
            stdout, stderr = await process.communicate()
            if stderr:
                raise Exception(stderr.decode())

            info["url"] = stdout.decode().split('\n')[1]

            # info["url"] = subprocess.run(
            #     f"yt-dlp --ignore-errors --get-url {weburl}", capture_output=True).stdout.decode()
            
            process = await asyncio.create_subprocess_shell(
                    f"yt-dlp --ignore-errors --get-title {weburl}", 
                    stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
            stdout, stderr = await process.communicate()
            if stderr:
                raise Exception(stderr.decode())

            # info["title"] = subprocess.run(
            #     f"yt-dlp --ignore-errors --get-title {weburl}", capture_output=True).stdout.decode()
            
            info["title"] = stdout.decode()

            return info
        except Exception as e:
            print(e)

