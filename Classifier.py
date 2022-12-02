import torch 
import torch.nn as nn
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from torch.nn import functional as function
from sklearn.metrics import accuracy_score
from torch.autograd import Variable
#from AudioAnalyzer import AudioAnalyzer as AA
from batcher import batcher 
import numpy as np

def output(x):
    x=function.softmax(x,dim=1)
    x=torch.max(x,dim=1)[1]
    x=x.data.numpy().squeeze()
    return x

class CNN(nn.Module):
    def __init__(self):
        super(CNN,self).__init__()
        self.conv1=nn.Sequential(
            nn.Conv2d(1,15,3,1,1).cuda(),#stride=1,padding=(kernel_size-1)/2=(3-1)/2=1 
            nn.ReLU().cuda(),
            nn.MaxPool2d(kernel_size=2).cuda()
            )
        self.conv2=nn.Sequential(
            nn.Conv2d(15,60,3,1,1).cuda(),
            nn.ReLU().cuda(),
            nn.MaxPool2d(kernel_size=2).cuda(),
            )
        self.nn1=nn.Linear(60*5*250,100).cuda()
        self.nn2=nn.Linear(100,2).cuda()
    def forward(self,x):
        x=self.conv1(x)
        x=self.conv2(x)
        #print(x.shape)
        x=x.view(x.size(0),-1)
        x=nn.functional.relu(self.nn1(x))
        x=self.nn2(x)
        return x
cnn=CNN()

torch.save(cnn,'Classification model.pt')
