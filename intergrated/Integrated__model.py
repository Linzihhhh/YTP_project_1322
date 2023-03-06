import torch
import numpy as np
from .AudioAnalyzer import AudioAnalyzer
from .batcher import batcher
import os


# import torch 
import torch.nn as nn
from torch.nn import functional as function

#from AudioAnalyzer import AudioAnalyzer as AA

class RNN(nn.Module):
    def __init__(self):
        super(RNN,self).__init__()
        self.rnn=nn.LSTM(20000,1000,5,batch_first=True)
        self.out=nn.Linear(1000,300)
        self.net=nn.Sequential(
            nn.Linear(300,50),
            nn.LeakyReLU(),
            nn.Linear(50,2)
            )
    def forward(self,x):
        x=x.to(torch.float32)
        r_out,(h_n,h_c)=self.rnn(x)
        x=self.out(r_out[:,-1,:])
        x=self.net(x)
        return x

class ANN(nn.Module):
    def __init__(self):
        super(ANN,self).__init__()
        self.nn1=nn.Linear(2, 100)
        self.nn2=nn.Linear(100,11)
    def forward(self,x):
        x=self.nn1(x)
        x=nn.functional.relu(x)
        x=self.nn2(x)
        x=nn.functional.softmax(x)
        
        return x

class mANN(nn.Module):
    def __init__(self):
        super(mANN,self).__init__()
        self.nn1=nn.Linear(2, 100)
        self.nn2=nn.Linear(100,11)
    def forward(self,x):
        x=self.nn1(x)
        x=nn.functional.relu(x)
        x=self.nn2(x)
        x=nn.functional.softmax(x)
        
        return x

class Rnn(nn.Module):
    def __init__(self):
        super(Rnn,self).__init__()
        self.rnn=nn.LSTM(20000,1000,5,batch_first=True)
        self.out=nn.Linear(1000,300)
        self.net=nn.Sequential(
            nn.Linear(300,200),
            nn.LeakyReLU(),
            nn.Linear(200,1)
            )
    def forward(self,x):
        x=x.to(torch.float32)
        r_out,(h_n,h_c)=self.rnn(x)
        x=self.out(r_out[:,-1,:])
        x=self.net(x)
        return x

class CNN(nn.Module):
    def __init__(self):
        super(CNN,self).__init__()
        self.conv1=nn.Sequential(
            nn.Conv2d(1,10,3,1,1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2)
            )
        self.conv2=nn.Sequential(
            nn.Conv2d(10,15,3,1,1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2)
            )
        self.linear=nn.Linear(600000,300)
        self.linear2=nn.Linear(300,2)
    def forward(self,x):
        x=x.to(torch.float32)
        x=self.conv1(x)
        x=self.conv2(x)
        x=x.view(-1,15*8*5000)
        x=self.linear(x)
        x=self.linear2(x)
        return x



class IntegratedTools:
    def __init__(self):
        
        self.aa=AudioAnalyzer()
        self.batcher=batcher()
        self.path = os.path.abspath(os.path.join(os.path.realpath(__file__),".."))
        print(self.path)
        return
    
    def output(self,x):
        x=torch.max(x,dim=1)[1]
        x=x.data.numpy().squeeze()
        return x
    
    def predict_classes(self,a_score,v_score,multi_classes=True,use_algorithm=1):
        
        if use_algorithm==1:
            '''use ANN for algorithm'''
            mann=torch.load(self.path+'/Models/multilabel_classifier.pt')
            matrix=np.matrix([[a_score,v_score]])
            matrix=mann(torch.from_numpy(matrix).float())
            
            if multi_classes==True:
                '''return each classes posibility'''
                return matrix.data.numpy()
            else:
                '''return the highest possible category, A=1,B=2....'''
                matrix=self.output(matrix)
                return matrix
        if use_algorithm==2:
            '''unfinished'''
            return
        
    def train_AVscore_model(self,data_path,user_arousal,user_valence,data_type=0):
        
        R=torch.load(f'{self.path}/Models/AVscore_predictor_rnn.pt')
        optim=torch.optim.Adam(R.parameters(),lr=0.01)
        loss_function=torch.nn.MSELoss()
        
        data=self.get_data(data_path,40)
        
        score=R(torch.FLoatTensor(data).view(-1,16,20000))
        loss=loss_function(torch.FloatTensor(score),torch.FloatTensor([user_arousal,user_valence]))
        
        loss.backward()
        optim.step()
        
        optim.zero_grad()
        return print('Train_successfully')
    
    def train_Liking_score_model(self,user_score,data_path,data_type=0):
        ''' input user_score and data_path to train the liking_score model'''
        
        R=torch.load(f'{self.path}/Models/likingscore_predict_model.pt')
        optim=torch.optim.Adam(R.parameters(),lr=0.001)
        loss_function=torch.nn.MSELoss()
        
        data=self.get_data(data_path, 40)
        
        optim.zero_grad()
        score=R(torch.FloatTensor(data).view(-1,16,20000))
        loss=loss_function(torch.FloatTensor(score),torch.FloatTensor([user_score]))
        
        loss.backward()
        optim.step()
        optim.zero_grad()
        
        torch.save(R,f'{self.path}/Models/likingscore_predict_model.pt')
        return print('Train_successfully')
    
    def predict_score(self,data,use_model=0):
        ''' 2=CQT with ANN, 1=MFCC+STFT with CNN 0= raw_data+RNN'''
        if use_model==0:
            rnn=torch.load(f'{self.path}/Models/AVscore_predictor_rnn.pt')
            matrix=rnn(torch.FloatTensor(data).view(-1,16,20000))
            matrix=matrix.data.numpy()
            return matrix
        if use_model==1:
            cnn=torch.load(f'self.path/Models/AVscore_predictor_cnn.pt')
            matrix=cnn(torch.from_numpy(data).view(1,1,32,20000))
            matrix=matrix.data.numpy()
            return matrix
            '''not finished'''
    
    def get_data(self,file_path,time_size,datatype=0):
        '''datatype 0=Raw data 1= Analyzed_ALL data, 2=CQT data'''
        '''please enter time_size with second'''
        if datatype==2:
            data=self.aa.analyze_ALL(file_path, time_size)
            return data
        
        if datatype==0:
            ''' mp3 only'''
            sr,data=self.aa.get_raw_data(file_path)
            data=data[:,0]
            data=data[:sr*time_size]
            return data
        
        if datatype==1:
            time_size=20000
            data=self.aa.analyze_ALL(file_path, time_size)
            return data
        
    def get_class_with_path(self,file_path,use_algorithm=0,time_size=40,n=3):
        '''0 RNN, 1 MFCC CNN, 2 CQT MLP'''
        
        data=self.get_data(file_path, time_size,use_algorithm)
        score=self.predict_score(data,use_algorithm)
        classes=self.predict_classes(score[0,0],score[0,1])
        return self.get_top_n_classes(classes,n)
    
        '''Classes type
            A=1:高興地，快樂的，充滿活力的 
            B=2:幽默的，輕鬆的，抒情的，愉快的
            C=3:放鬆的，輕柔的，優美的，優雅的，安詳的
            D=4:傷感的，哀愁的
            E=5:悲慘的，傷心絕望的
            F=6:使人感到壓抑的，憂鬱的，沮喪的
            G=7:雄偉的，沉重的，嚴肅的
            H=8:激動人心的，激動萬分的，刺激的，歡欣鼓舞的
            I=9:緊張的，焦躁不安的
            J=10:惱怒的，憤憤不平的
            K=11:高潔的，有志氣的
        '''
    def get_top_n_classes(self,data,n=3):
        que=[]
        i=1
        for j in data[0]:
            que.append((j*100,i))
            i+=1
        que.sort(reverse=True)
        return que
        
    def Get_Liking_score_with_path(self,path,data_type=0):
        '''data_type=0 raw_data, =1 AnalyzedAll_data, =2 CQT data'''
        if data_type==0:
            data=self.get_data(path, 40)
            R=torch.load(self.path+'/Models/likingscore_predict_model.pt')
            matrix=R(torch.FloatTensor(data).view(-1,16,20000))
            score=matrix.data.numpy()
            return score
            
    def class_and_score(self,path,data_type=0):
        
        c=self.get_class_with_path(path,data_type)
        score=self.Get_Liking_score_with_path(path,data_type)
        return c,score
