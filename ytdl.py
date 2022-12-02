import os
import subprocess
import json

class YoutubeMusicDownloader:
    def __init__(self):
        pass
    
    def download(self, url: str, *, path: str = None):
        try:
            path = path or os.getcwd()

            process = subprocess.run(
                f"yt-dlp --ignore-errors --extract-audio --audio-format wav -o \"{path}/%(id)s.wav\" {url}")
        except Exception as e:
            print(e)

    def fetch_comments(self, url: str, *, path: str = None):
        try:
            path = path or os.getcwd()

            process = subprocess.run(
                f'yt-dlp --ignore-errors --get-id "{url}"', capture_output = True)
            
            ids = process.stdout.decode().split('\n')
            ids.pop() # remove the last empty string

            for id in ids:
                filename = path + "/" + id
                process = subprocess.run(
                    f'yt-dlp --ignore-errors --write-comments --no-download -o "{filename}" "https://www.youtube.com/watch?v={id}"')

                with open(f"{id}.info.json", "r") as f:
                    data = json.load(f)

                data = data["comments"]
                
                with open(f"{id}.json", "w") as f:
                    json.dump(data, f)
                
                os.remove(f"{filename}.info.json")

        except Exception as e:
            print(e)
    
# ytdl = YoutubeMusicDownloader()
# ytdl.download("$video/playlist")
# ytdl.fetch_comments("$playlist")
# ytdl.fetch_comments("$video")