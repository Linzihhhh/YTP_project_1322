import torch
import numpy as np
from AudioAnalyzer import AudioAnalyzer
from Models_module import mANN,ANN,RNN
from batcher import batcher

class IntegratedModel:
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
            '''un finished'''
            return
        
    def train_classify_model(self,):
        return
    
    def train_all_model(self):
        return 
    def predict_score(self,data,use_model=0):
        ''' 2=CQT with ANN, 1=MFCC+STFT with CNN 0= raw_data+RNN'''
        
        return 
    
    def get_data(self,file_path,time_size,datatype=0):
        '''datatype 0=Raw data 1= Analyzed_ALL data, 2=CQT data'''
        if datatype==1:
            data=self.aa.analyze_ALL(file_path, time_size)
            return data
        
        if datatype==0:
            data=self.aa.get_raw_data(file_path)
            return data
        if datatype==2:
            data=self.aa.analyze_CQT(file_path, time_size)
            return
        
       
    
    
        
    
        
            
    

        
    