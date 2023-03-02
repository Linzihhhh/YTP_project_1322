import numpy as np

class batcher:
    def __init__(self):
        return
    def batch(self,data,batch_size,message=False):
        data_list=[]
        while(data.shape[0]>=batch_size):
            x,data=np.vsplit(data,[batch_size])
            data_list.append(x)
            #print(x.shape)
        if(message==True):
            if(data.shape[0]>0):
                p=data.shape[0]    
                print(f'{p} datas cannot be batched')
            else:
                print('batched succefully')
            
        batched_data=np.array(data_list)
        return batched_data
    
    def batch_all(self,x_data,y_data,batch_size,message=False):
        
        batch_x=self.batch(x_data,batch_size,message)
        batch_y=self.batch(y_data,batch_size,message)
        
        return batch_x,batch_y
    def get_sequent_with_single_label(self,y,length):
        seq_y=np.zeros((y.shape[0],length))
        for i in range(y.shape[0]):
            seq_y[i][y[i]]=1
        return seq_y
    
