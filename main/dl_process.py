from ytdl import YoutubeMusicDownloader
from AudioAnalyzer import AudioAnalyzer
import os, time
import numpy as np


ytdl = YoutubeMusicDownloader()
alr = AudioAnalyzer()

urls = ['https://www.youtube.com/watch?v=B7xai5u_tnk'] #new song url list
timestr = time.strftime("%Y%m%d-%H%M%S")

for url in urls:
    ytdl.download(url,path = os.path.dirname(os.path.realpath(__file__)) + r'\trainingsong') #download all songs

songs = os.listdir(os.path.dirname(os.path.realpath(__file__)) + r'\trainingsong') #get the song list

lists = []
for song in songs:
    data = alr.analyze_ALL(os.path.dirname(os.path.realpath(__file__)) + f'/trainingsong/{song}',1000)
    lists.append(data)

all_data = np.array(lists) 
print(all_data.shape)
alr.save(all_data, os.path.dirname(os.path.realpath(__file__)) + r'\audiodata' + f'/{timestr}') #generate a numpy