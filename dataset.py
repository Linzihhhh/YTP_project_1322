from ytdl import YoutubeMusicDownloader
from AudioAnalyzer import AudioAnalyzer
import os, time
import numpy as np


class Dataset:
    def __init__(self):
        self.ytdl = YoutubeMusicDownloader()
        self.alr = AudioAnalyzer()
        self.unbatch_path = os.getcwd() + '/audiodata/unbatch/'
        self.music_path = os.getcwd() + '/trainingsong/'
        self.batched_path = os.getcwd() + '/audiodata/batched/'
        if not os.path.exists(self.unbatch_path):
            os.makedirs(self.unbatch_path)
        if not os.path.exists(self.music_path):
            os.makedirs(self.music_path)
        if not os.path.exists(self.batched_path):
            os.makedirs(self.batched_path)
    
    def download(self, url:str):
        self.ytdl.download(url,root = self.music_path)
    
    def downloads(self, urls:list):
        for url in urls:
            self.ytdl.download(url,path = self.music_path)
    
    def general_music_data(self):
        timestr = time.strftime("%Y%m%d-%H%M%S")
        folders = os.listdir(self.music_path)
        lists = []
        for folder in folders:
            path = self.music_path + folder + '/' + folder + '.wav'
            data = self.alr.analyze_MFCC(path, 1000)
            lists.append(data)
        
        try:
            old_datas = os.listdir(self.unbatch_path)
            for old_data in old_datas:
                os.remove(self.unbatch_path + old_data)
        except:
            pass
        
        all_data = np.array(lists)
        print("all music have batched! shape=" + all_data.shape)
        
        np.save(self.unbatch_path + timestr, all_data)
    

    def batch(self,batch_size,message=False):
        data_list=[]
        timestr = time.strftime("%Y%m%d-%H%M%S")

        dataname = os.listdir(self.unbatch_path)
        data_path = self.unbatch_path + dataname[0]

        data = np.load(data_path)
        print('successfully load the unbatch file, shape = ',end='')
        print(data.shape)

        while(data.shape[0]>=batch_size):
            x,data=np.vsplit(data,[batch_size])
            data_list.append(x)
            #print(x.shape)
        if(message==True):
            if(data.shape[0]>0):
                p=data.shape[0]    
                print(f'{p} datas cannot be batched')
            else:
                print('batched succefully')
            
        batched_data=np.array(data_list)
        
        np.save(self.batched_path + timestr, batched_data)





