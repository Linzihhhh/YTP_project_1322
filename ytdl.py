import os
import subprocess

class YoutubeMusicDownloader:
    def __init__(self):
        pass
    
    def download(self, url: str, *, path=None):
        try:
            path = path or os.getcwd()

            process = subprocess.run(
                f"youtube-dl -i --extract-audio --audio-format wav -o \"{path}/%(title)s-%(id)s.wav\" {url}")
            process.check_returncode()
        except Exception as e:
            print(e)
    
# ytdl = YoutubeMusicDownloader()
# ytdl.download("[URL]")



