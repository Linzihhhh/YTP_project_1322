import os
import subprocess

class YoutubeMusicDownloader:
    def __init__(self):
        pass
    
    def generate_title(self, url: str):
        process = subprocess.run(f"youtube-dl --get-id \"{url}\"", capture_output=True)
        process.check_returncode()
        id = process.stdout.decode().strip()
        print(id)
        process = subprocess.run(f"youtube-dl --get-title \"{url}\"", capture_output=True)
        process.check_returncode()
        title = process.stdout.decode().strip()
        return title + " - " + id

    def download(self, url: str, *, path=None, title=None):
        try:
            path = path or os.getcwd()
            title = title or self.generate_title(url)

            process = subprocess.run(f"youtube-dl --extract-audio --audio-format wav -o \"{path}\\{title}.wav\" \"{url}\"")
            process.check_returncode()

        except Exception as e:
            print(e)
            
    
ytdl = YoutubeMusicDownloader()
ytdl.download("https://www.youtube.com/watch?v=5MWdriB3EBM")