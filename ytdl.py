import os
import subprocess
import json

class YoutubeMusicDownloader:
    def __init__(self):
        pass

    def get_ids(self, url: str) -> list:
        try:
            process = subprocess.run(
                f'yt-dlp --ignore-errors --get-id "{url}"', capture_output = True)
            
            ids = process.stdout.decode().split('\n')
            ids.pop() # remove the last empty string
            return ids
        except Exception as e:
            print(e)
    
    def download_song(self, id: str, *, path: str = None): 
        """
        Download a video
        """

        try:
            url = f"https://www.youtube.com/watch?v={id}"
            path = path or os.getcwd()

            process = subprocess.run(
                f"yt-dlp --ignore-errors --extract-audio --audio-format wav -o \"{path}/%(id)s.wav\" {url}")
        except Exception as e:
            print(e)

    def fetch_comment(self, id: str, *, path: str = None, max_comments: int = 2000, max_replies: int = 0):
        """
        Download comments from a video
        """

        try:
            url = f"https://www.youtube.com/watch?v={id}"

            filename = path + "/" + id
            process = subprocess.run(
                f'yt-dlp --ignore-errors --write-comments --no-download -o "{filename}" {url} --extractor-args "youtube:max-comments={max_comments},all,{max_replies},all";')

            with open(f"{filename}.info.json", "r") as f:
                data = json.load(f)

            data = data["comments"]
            
            with open(f"{filename}.json", "w") as f:
                json.dump(data, f)
            
            os.remove(f"{filename}.info.json")

        except Exception as e:
            print(e)

    def download(self, url: str, *, root: str = None):
        """
        Download video/playlist from a given url
        """
        try:
            root = root or os.getcwd()

            ids = self.get_ids(url)
            for id in ids:
                try:
                    path = root + "/" + id
                    os.mkdir(path)
                    
                    self.download_song(id, path = path)
                    self.fetch_comment(id, path = path)
                except Exception as e:
                    print(e)

        except Exception as e:
            print(e)
    
# ytdl = YoutubeMusicDownloader()
# ytdl.download("$video/playlist")