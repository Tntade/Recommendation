
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd


# In[2]:


from MostPopular import MostPopular
from UserCF import UserCF
from ItemCF import ItemCF
from LFM import LFM
from Data import Data


# In[3]:


#交集融合的话，那么在每个算法中的N=7，做交集融合后的N可以选择为3，4
class andEnsemble:  #交集融合法
    def __init__(self,data):
        self.rec_algs=[UserCF,ItemCF,LFM]
        
        self.data=data
        
        self.k=None
        self.n=None
        self.N=None

        self.recommendation=None
    
    def compute_recommendation(self,k=20,n=10,N=3):
        self.k=k
        self.N=N
        self.n=n #本交集融合后推荐的个数，必然n<N
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
        
        recs={}
        for user in rank:
            if user not in recs:
                recs[user]=[]
            for item in rank[user]:
                if rank[user][item]==3:
                    recs[user].append(item)
            if len(recs[user])<self.n:
                dif=self.n-len(recs[user])
                ranked_rank=[x[0] for x in sorted(rank[user].items(),key=lambda x:x[1],reverse=True)]
                make_up_item=[x for x in ranked_rank if x not in recs[user]][:dif]
                recs[user].append(item)
        recs={u:v[:self.N] for u,v in recs.items()}
        return recs


# In[4]:


# if __name__=='__main__':
#     dt=Data()
#     andEns=andEnsemble(dt)
#     andEns.compute_recommendation()
#     for user in dt.old_users:
#         print(user)
#         print(andEns.recommendation[user])
#         print('_'*20)

