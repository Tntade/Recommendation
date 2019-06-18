
# coding: utf-8

# In[9]:


import numpy as np
import pandas as pd


# In[10]:


from Data import Data


# In[11]:


from MostPopular import MostPopular
from UserCF import UserCF
from ItemCF import ItemCF
from LFM import LFM


# In[12]:


class linearEnsemble:  #将得到的模型成绩放到df中
    def __init__(self,data):
        self.rec_algs=[UserCF,ItemCF,LFM]
        
        self.data=data
        
        self.k=None
        self.n=None
        
        self.N=None
        self.algs_dic=None
        self.linear_w_dic=None 
        self.recommendation=None
    
    def compute_recommendation(self,linear_w_dic={'UserCF':0.3,'ItemCF':0.4,'LFM':0.3},k=10,n=8,N=5):
        self.k=k
        self.n=n
        
        self.N=N
        self.linear_w_dic=linear_w_dic
        self.recommendation=self.__get_recommendation()
    
    def __get_recommendation(self):
        rank={} 
        
        for alg in self.rec_algs[:2]:
            recommend=alg(self.data)
            recommend.compute_recommendation(self.k,self.n)
            for user in self.data.users:
                if user not in rank:
                    rank[user]={}
                rec_list=recommend.recommendation[user]
                for item in rec_list:
                    if item not in rank[user]:
                        rank[user][item]=(1*self.linear_w_dic[alg.__name__]) 
                    rank[user][item]+=self.linear_w_dic[alg.__name__]
        alg=self.rec_algs[2]
        recommend=alg(self.data)
        recommend.compute_recommendation(self.n)
        for user in rank:
            for item in recommend.recommendation[user]:
                if item not in rank[user]:
                    rank[user][item]=(1*self.linear_w_dic[alg.__name__]) 
                rank[user][item]+=self.linear_w_dic[alg.__name__]
        rank={u:[x[0] for x in sorted(v.items(),key=lambda x:x[1],reverse=True)[:self.N]] for u,v in rank.items()}
        return rank           


# In[13]:


# if __name__=='__main__':
#     dt=Data()
#     linear=linearEnsemble(dt)
#     linear.compute_recommendation()

#     for user in dt.old_users:
#         print(user)
#         print(linear.recommendation[user])
#         print('-'*20)

