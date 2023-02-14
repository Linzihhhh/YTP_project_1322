import torch
import numpy as np
import pandas as pd
import torch.nn as nn
import torch.nn.functional as function 
from batcher import batcher

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
'''
ann=mANN()
f=pd.read_csv('Categories data.csv')
data=f.to_numpy()
x=data[:,:2]
y=data[:,2]
bat=batcher()

optimizer=torch.optim.Adam(ann.parameters(),lr=0.001)
loss_function=torch.nn.BCELoss()
Epochs=5000

y=bat.get_sequent_with_single_label(y, 11)

x=torch.from_numpy(x)
y=torch.from_numpy(y)
x=x.float()
y=y.float()
for i in range(Epochs):
    optimizer.zero_grad()
    y_pred=ann(x)
    loss=loss_function(y_pred,y)
    loss.backward()
    optimizer.step()
y_pred=ann(x)
print(y_pred[0].data.numpy())
torch.save(ann,'Multiple-Labeled classifier.pt')
'''

