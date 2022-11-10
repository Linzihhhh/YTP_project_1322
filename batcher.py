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
    
