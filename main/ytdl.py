from __future__ import unicode_literals
import yt_dlp, urllib.error

class YoutubeMusicDownloader:
    def __init__(self):
        self.ydl_opts = {
            'format': 'bestaudio', # test
            'outtmpl': 'main\music\%(title)s.%(ext)s',
            # 'outtmpl': '%(extractor_key)s\%(title)s.mp3',
            'default_search': 'auto',
            # 'cookiefile': 'youtube.com_cookies.txt', # <- this can download age-restricted video
        }

    def download(self, url: str):
        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            try:
                ydl.download([url])
            except yt_dlp.utils.DownloadError as DownloadError:
                if type(DownloadError.exc_info[1]) == urllib.error.URLError:
                    print('Unknown Url')
                elif type(DownloadError.exc_info[1]) == yt_dlp.utils.ExtractorError:
                    print('Join this channel to get access to members-only content like this video, and other exclusive perks.')
            except Exception as ex:
                print('\n', type(ex).__name__)