import torch
import torch.nn as nn
from sklearn.metrics import accuracy_score
import numpy as np
import pandas as pd
def output(x):
    x=torch.max(x,dim=1)[1]
    x=x.data.numpy().squeeze()
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
    
ann=ANN()
f=pd.read_csv('Categories data.csv',dtype=float)
data=f.to_numpy()
x=data[:,:2]
y=data[:,2]

optimizer=torch.optim.Adam(ann.parameters(),lr=0.001)
loss_function=torch.nn.CrossEntropyLoss()
Epochs=5000

x=torch.from_numpy(x)
y=torch.from_numpy(y)
x=x.float()
y=y.float()
for i in range(Epochs):
    optimizer.zero_grad()
    y_pred=ann(x)
    loss=loss_function(y_pred,y.long())
    loss.backward()
    optimizer.step()
y_pred=ann(x)
print(accuracy_score(y, output(y_pred)))
torch.save(ann,'SingleLabeledANN.pt')

