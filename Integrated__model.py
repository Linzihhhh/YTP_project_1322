import torch
import numpy as np
from AudioAnalyzer import AudioAnalyzer
from Models_module import mANN,ANN,RNN,Rnn
from batcher import batcher


class IntegratedTools:
    def __init__(self):
        
        self.aa=AudioAnalyzer()
        self.batcher=batcher()
        return
    
    def output(self,x):
        x=torch.max(x,dim=1)[1]
        x=x.data.numpy().squeeze()
        return x
    
    def predict_classes(self,a_score,v_score,multi_classes=True,use_algorithm=1):
        
        if use_algorithm==1:
            '''use ANN for algorithm'''
            mann=torch.load('Models/multilabel_classifier.pt')
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
        
    def train_classify_model(self,):
        return
    
    def train_all_model(self):
        return 
    
    def predict_score(self,data,use_model=0):
        ''' 2=CQT with ANN, 1=MFCC+STFT with CNN 0= raw_data+RNN'''
        if use_model==0:
            rnn=torch.load('Models/AVscore_predictor_rnn.pt')
            matrix=rnn(torch.FloatTensor(data).view(-1,18,20000))
            matrix=matrix.data.numpy()
            return matrix
        if use_model==1:
            '''not finished'''
    
    def get_data(self,file_path,time_size,datatype=0):
        '''datatype 0=Raw data 1= Analyzed_ALL data, 2=CQT data'''
        '''please enter time_size with second'''
        if datatype==1:
            data=self.aa.analyze_ALL(file_path, time_size)
            return data
        
        if datatype==0:
            ''' mp3 only'''
            sr,data=self.aa.get_raw_data(file_path)
            data=data[:,0]
            data=data[:sr*time_size]
            return data
        
        if datatype==2:
            
            data=self.aa.analyze_CQT(file_path, time_size)
            return data
        
    def get_class_with_path(self,file_path,use_algorithm=0,time_size=45,n=3):
        '''0 RNN, 1 MFCC CNN, 2 CQT MLP'''
        
        data=self.get_data(file_path, time_size)
        score=self.predict_score(data)
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
        
    def Get_Liking_score_with_path(self,data,data_type=0):
        '''data_type=0 raw_data, =1 AnalyzedAll_data, =2 CQT data'''
        if data_type==0:
            data=self.get_data(data, 45)
            Rnn=torch.load('Models/likingscore_predict_model.pt')
            matrix=Rnn(torch.FloatTensor(data).view(-1,18,20000))
            score=matrix.data.numpy()
            return score
            
aa=IntegratedTools()
print(aa.Get_Liking_score_with_path('Local/Youtube/1.mp3'))
print()
        
        
       
    
    
        
    
        
            
    

        
    