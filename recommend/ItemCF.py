
# coding: utf-8

# In[10]:


from Data import Data
from MostPopular import MostPopular


# In[11]:


class ItemCF:
    def __init__(self,data):
        self.data=data
        
#         self.mp=MostPopular
        self.item_sim=self.__item_sim() #找到相似item
        
        self.K=None
        self.N=None
        self.Q=None
        self.recommendation=None
    
    def compute_recommendation(self,K=15,N=5):
        self.K=K
        self.N=N
        self.recommendation=self.__get_recommendation()
    
    def __item_sim(self):
        tmp=self.data.train[['item','industry_str','item_label_1','item_label_2']].values
        item_label={}
        item_sim={}
        for i in range(len(tmp)):
            item=tmp[i][0]
            label3=tmp[i][1]
            label1=tmp[i][2]
            label2=tmp[i][3]
            if item not in item_label:
                item_label[item]=0
            item_label[item]=[]
            if label1 not in item_label[item]:
                item_label[item].append(label1)
            if label2 not in item_label[item]:
                item_label[item].append(label2)
            if label3 not in item_label[item]:
                item_label[item].append(label3)
        
        for u in item_label:
            u_label=item_label[u]
            if u not in item_sim:
                item_sim[u]={}
            for v in item_label:
                if u==v:continue
                v_label=item_label[v]
                count=0
                for label in u_label:
                    if label in v_label:
                        count+=1
                item_sim[u][v]=count/(len(u_label)*len(v_label))
        item_sim={u:sorted(v.items(),key=lambda x:x[1],reverse=True) for u,v in item_sim.items()} 
#         print("item_sim:",item_sim)
        return item_sim 
    
    def __recommend(self,user): 
        if user in self.data.dic:
            rank={}
            if 0 not in self.data.dic[user]:
                seen_item=[]
            else:
                seen_item=self.data.dic[user][0]
#                 print(seen_item)
                for item in seen_item:
                    sim_items=[x[0] for x in self.item_sim[item][:self.K]]
                    for it in sim_items:
                        if it not in rank:
                            rank[it]=0
                        rank[it]+=1
                rank=sorted(rank.items(),key=lambda x:x[1],reverse=True)
                rank=[x for x in [y[0] for y in rank] if x not in seen_item][:self.N]
#                 print(user)
#                 print(rank)
        else:
            mp=MostPopular(self.data)
            mp.compute_recommendation()
            rank=mp.recommendation[user][:self.N]
#             print(user)
#             print(rank)
        return rank
        
    def __get_recommendation(self):
        recs={}
        for user in self.data.users:
            if user not in recs:
                recs[user]=[]
            recs[user]=self.__recommend(user)
        return recs


# In[12]:


# if __name__=='__main__':
#     dt=Data()
#     iff=ItemCF(dt)
#     iff.compute_recommendation()

