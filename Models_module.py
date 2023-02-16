import torch 
import torch.nn as nn
from torch.nn import functional as function

#from AudioAnalyzer import AudioAnalyzer as AA

class RNN(nn.Module):
    def __init__(self):
        super(RNN,self).__init__()
        self.rnn=nn.LSTM(40000,800,5,batch_first=True)
        self.out=nn.Linear(800,300)
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



        
        

