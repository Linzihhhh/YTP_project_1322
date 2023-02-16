from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
f=pd.read_csv('Categories data.csv')
data=f.to_numpy()
print(data.shape)
y=data[:,2]
x=data[:,:2]
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.1,random_state=10)
knn=KNeighborsClassifier(n_neighbors=10)
knn.fit(x_train,y_train)
y_pred=knn.predict(x_test)

joblib.dump(knn,'knn.pkl')

