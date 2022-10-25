from ytdl import YoutubeMusicDownloader as yl
from AudioAnalyzer import AudioAnalyzer
import os

ytdl = yl()

alr = AudioAnalyzer()

print(os.path.dirname(os.path.realpath(__file__)) + r"\song\unity.wav")


data = alr.analyze_STFT(os.path.dirname(os.path.realpath(__file__)) + r"\song\unity.wav",1000)
print(data.shape)
alr.save(data, os.path.dirname(os.path.realpath(__file__)) + r"\audiodata\hello")