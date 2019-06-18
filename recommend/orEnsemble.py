
# coding: utf-8

# In[5]:


from Data import Data
from MostPopular import MostPopular
from UserCF import UserCF
from ItemCF import ItemCF
from LFM import LFM


# In[6]:


import pandas as pd
import numpy as np


# In[7]:


class orEnsemble:  #并集融合
    def __init__(self,data):
        self.rec_algs=[UserCF,ItemCF,LFM]
        
        self.data=data
        
        self.k=None
        self.n=None
        
        self.N=None
        self.recommendation=None
        
    def compute_recommendation(self,k=15,n=7,N=3):
        self.k=k
        self.n=n
        self.N=N
        self.recommendation=self.__get_recommendation()
    
    def __get_recommendation(self):
        rank={}
        for alg in self.rec_algs[:2]:
#             print(alg.__name__)
            recommend=alg(self.data)
            recommend.compute_recommendation(self.k,self.n)
            for user in self.data.users:
                if user not in rank:
                    rank[user]={}
                rec_list=recommend.recommendation[user]
                for item in rec_list:
                    if item not in rank[user]:
                        rank[user][item]=1
                    rank[user][item]+=1
        
        alg=self.rec_algs[2]
#         print(alg.__name__)
        recommend=alg(self.data)
        recommend.compute_recommendation(self.n)
        for user in rank:
            for item in recommend.recommendation[user]:
                if item not in rank[user]:
                    rank[user][item]=1
                rank[user][item]+=1
        ranked_rank={u:[x[0] for x in sorted(v.items(),key=lambda x:x[1],reverse=True)[:self.N]] for u,v in rank.items()}
        return ranked_rank


# In[8]:


# if __name__=='__main__':
#     dt=Data()
#     orEns=orEnsemble(dt)
#     orEns.compute_recommendation()
#     for user in dt.old_users:
#         print(user)
#         print(orEns.recommendation[user])
#         print('-'*20)

