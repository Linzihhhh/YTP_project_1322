import torch
import numpy as np
from AudioAnalyzer import AudioAnalyzer
from Models_module import mANN,ANN,RNN
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
    
    def get_classes(self,a_score,v_score,multi_classes=True,use_algorithm=1):
        
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
            return
    def get_class_with_path(self,file_path,use_algorithm=0,time_size=45):
        '''0 RNN, 1 MFCC CNN, 2 CQT MLP'''
        
        data=self.get_data(file_path, time_size)
        score=self.predict_score(data)
        print(score)
        classes=self.get_classes(score[0,0],score[0,1])
        return classes

aa=IntegratedTools()
print(aa.get_class_with_path('Local/Youtube/1.mp3'))
        
        
       
    
    
        
    
        
            
    

        
    