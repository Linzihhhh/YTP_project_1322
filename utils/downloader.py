from typing import *

import os
import subprocess
import asyncio
import aiohttp

class YoutubeDownloader:

    @classmethod
    async def get_ids(cls, url: str) -> list:
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
    async def get_info(cls, id: str, *, path: str = None): 
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
                    f"yt-dlp -i -g {weburl}", 
                    stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
            stdout, stderr = await process.communicate()
            if stderr:
                raise Exception(stderr.decode())

            info["url"] = stdout.decode().split('\n')[1]

            # info["url"] = subprocess.run(
            #     f"yt-dlp --ignore-errors --get-url {weburl}", capture_output=True).stdout.decode()
            
            process = await asyncio.create_subprocess_shell(
                    f"yt-dlp -i -e {weburl}", 
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

    @classmethod
    async def download(cls, id: str, path=None, **opts):
        path = path or os.getcwd()

        try:
            weburl = f"https://www.youtube.com/watch?v={id}"
            path = path or os.getcwd()

            process = await asyncio.create_subprocess_shell(
                    f"yt-dlp -i -g -f wa {weburl}", 
                    stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
            stdout, stderr = await process.communicate()
            if stderr:
                raise Exception(stderr.decode())

            url = stdout.decode().strip()

            ss = opts.get("ss") or "00:00:00.00"
            t = opts.get("t") or "00:00:45.00"

            process = await asyncio.create_subprocess_shell(
                    f"ffmpeg -ss {ss} -i \"{url}\" -t {t} -n {path}/{id}.mp3", 
                    stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
            stdout, stderr = await process.communicate()
            if stderr:
                raise Exception(stderr.decode())

        except Exception as e:
            print(e)