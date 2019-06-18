
# coding: utf-8

# In[1]:


from Data import Data
from UserCF import UserCF
from ItemCF import ItemCF
from MostPopular import MostPopular
from LFM import LFM

from linearEnsemble import linearEnsemble
from andEnsemble import andEnsemble
from orEnsemble import orEnsemble


# In[2]:


class thirdLevelEnsemble: 
    def __init__(self,data):
        self.data=data
        self.rec_algs=[linearEnsemble,andEnsemble,orEnsemble]
        
#         self.k=None #启用原代码中的数值就可以了,所以不用设置
#         self.n=None
#         self.N=None
        
        self.fin=None
        self.recommendation=None
        
    def compute_recommendation(self,fin=3):
        self.fin=fin
        self.recommendation=self.__get_recommendation()
    
    def __get_recommendation(self): 
        rank={}
        
        alg=self.rec_algs[0]
#         print(alg.__name__)
        recommend=alg(self.data)
        recommend.compute_recommendation()
        for user in self.data.users:
            if user not in rank:
                rank[user]={}
            rec_list=recommend.recommendation[user]
            for item in rec_list:
                if item not in rank[user]:
                    rank[user][item]=1
                rank[user][item]+=1        
        
        for i in range(1,3):
            alg=self.rec_algs[i]
#             print(alg.__name__)
            recommend=alg(self.data)
            recommend.compute_recommendation()
            for user in self.data.users:
                if user not in rank:
                    rank[user]={}
                rec_list=recommend.recommendation[user]
                if len(rec_list)>0:
                    for item in rec_list:
                        if item not in rank[user]:
                            rank[user][item]=1
                        rank[user][item]+=1
                else:continue
        rank={u:[x[0] for x in sorted(v.items(),key=lambda x:x[1],reverse=True)[:self.fin]] for u,v in rank.items()}
        return rank 


# In[3]:


# if __name__=='__main__':
#     dt=Data()
#     tle=thirdLevelEnsemble(dt)
#     tle.compute_recommendation()
#     for user in dt.old_users:
#         print(user)
#         print(tle.recommendation[user])
#         print('-'*20)

