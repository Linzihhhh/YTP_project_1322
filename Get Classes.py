import torch
import numpy as np
from AudioAnalyzer import AudioAnalyzer
from singlelabel_classifier import ANN 
from multilabel_classifier import mANN
from sklearn.neighbors import KNeighborsClassifier
import joblib

class IntegratedModel:
    def __init__(self):
        
        aa=AudioAnalyzer()
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
        
    def train_model(self):
        return
    
    def train_all_model(self):
        return
    
    def get_data(self):
        return
    
    def predict_avscore(self):
        return
    
    
        
    
        
            
    

        
    