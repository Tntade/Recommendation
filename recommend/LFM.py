
# coding: utf-8

# In[28]:


import numpy as np
import pandas as pd

from Data import Data
from MostPopular import MostPopular


# In[29]:


class LFM:
    def __init__(self,data):
        self.data=data
        
        self.new_data=self.__get_samples() #负采样
        self.N=None
        self.F=None
        self.steps=None
        self.lr=None
        self.lmbda=None
         
        self.recommendation=None
    
    def compute_recommendation(self,N=5,F=20,steps=30,lr=0.01,lmbda=0.02):
        self.N=N
        self.F=F
        self.steps=steps
        self.lr=lr
        self.lmbda=lmbda
        self.P,self.Q=self.__get_PQ()   
        self.recommendation=self.__get_recommendation()
        
    def __get_samples(self):
        new_data={}  
        for user in self.data.dic:
            if user not in new_data:
                new_data[user]={}
            if 0 in self.data.dic[user]:
                buy_items=self.data.dic[user][0]
                for item in buy_items:
                    new_data[user][item]=1
            if 1 in self.data.dic[user]:
                quote_items=self.data.dic[user][1]
                for it in quote_items:
                    new_data[user][it]=0
        
        #防止空列表出现，所以进行负采样
        ranked_item_pop=sorted(self.data.item_pop.items(),key=lambda x:x[1],reverse=True)
        item_pops=[x[0] for x in ranked_item_pop]
        for user in new_data:
            pos=0
            neg=0
            for item in new_data[user]:
                if new_data[user][item]==1:
                    pos+=1
                elif new_data[user][item]==0:
                    neg+=1
            if pos>neg:
                dif=pos-neg #需要补充的负采样数量
                neg_samples=[x for x in item_pops if x not in new_data[user]][:dif]
                for it in neg_samples:
                    if it not in new_data[user]:
                        new_data[user][it]=0
            else:
                continue
        return new_data #正负样本数据相等的采样方式

    
    def __get_PQ(self):
        P={} # user_k
        Q={} #k_item
        for user in self.data.train_users:
            P[user]=np.random.random(self.F) #假设有ｆ个隐语义
        for item in self.data.train_items:
            Q[item]=np.random.random(self.F)
        
        for i in range(self.steps):
            for user in self.new_data:
                for item in self.new_data[user]:
                    eui=self.new_data[user][item]-(P[user]*Q[item]).sum()
                    P[user]+=self.lr*(Q[item]*eui-self.lmbda*P[user])
                    Q[item]+=self.lr*(P[user]*eui-self.lmbda*Q[item])
            self.lr*=0.9
        return P,Q    
    
    def __recommend(self,user):
        W={}
        if user in self.data.dic:
            if 0 in self.data.dic[user]:
                seen_item=self.data.dic[user][0]
            else:seen_item=[]  
            rec_item=[x for x in self.data.train_items if x not in seen_item]
            for item in rec_item:
                if item not in W:
                    W[item]=0
                W[item]=(self.P[user]*self.Q[item]).sum()
            rank=[x[0] for x in sorted(W.items(),key=lambda x:x[1],reverse=True)[:self.N]]
        else:
            mp=MostPopular(self.data)
            mp.compute_recommendation()
            rank=mp.recommendation[user][:self.N]
        return rank
        

    def __get_recommendation(self):
        recs={}
        for user in self.data.users:
            if user not in recs:
                recs[user]=[]
            recs[user]=self.__recommend(user)
        return recs


# In[30]:


# if __name__=='__main__':
#     dt=Data()
#     lfm=LFM(dt)
#     lfm.compute_recommendation()
#     for user in dt.old_users:
#         print(user)
#         print(lfm.recommendation[user])
#         print('_'*20)

