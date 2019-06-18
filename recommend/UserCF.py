
# coding: utf-8

# In[1]:


from Data import Data
from MostPopular import MostPopular


# In[2]:


class UserCF:
    def __init__(self,data):
        self.data=data
        
#         self.mp=MostPopular
        self.user_sim=self.__user_sim()
        
        self.K=None
        self.N=None
        self.recommendation=None
    
    def compute_recommendation(self,K=10,N=5): #K一定要多放一些，不然去掉user已经buy的就剩下不了多少item了
        self.K=K
        self.N=N
        self.recommendation=self.__get_recommendation()
    
    def __user_sim(self):     
        user_label={}   #{user:[label,label]}
        tmp=self.data.train[['user','industry_str','item_label_1']].values
        for i in range(len(tmp)):
            user=tmp[i][0]
            label1=tmp[i][1]
            label2=tmp[i][2]
            if user not in user_label:
                user_label[user]=[]
            if label1 not in user_label[user]:
                user_label[user].append(label1)
            if label2 not in user_label[user]:
                user_label[user].append(label2)
        
        user_sim={}    #return: {u:{v1:sim1,v2:sim2,,},u2:{},,,}
        for u in user_label:
            u_label=user_label[u]
            if u not in user_sim:
                user_sim[u]={}
            for v in user_label:
                if u==v:continue
                v_label=user_label[v]
                count=0
                for item in u_label:
                    if item in v_label:
                        count+=1
                user_sim[u][v]=count/(len(u_label)*len(v_label))
        user_sim={u:sorted(v.items(),key=lambda x:x[1],reverse=True) for u,v in user_sim.items()}
        return user_sim
    
    def __recommend(self,user): #recommend for one user
        if user in self.data.dic:
            if 0 in self.data.dic[user]:
                seen_item=self.data.dic[user][0]
            else:seen_item=[]
            if user in self.user_sim:
                rank={}
                sim_dic=self.user_sim[user][:self.K] #选择最相似度的topk用户
                for v in [x[0] for x in sim_dic]:
                    if 0 in self.data.dic[v]:
                        v_seen_item=self.data.dic[v][0]
                    else:v_seen_item=[]
                    for item in [x for x in v_seen_item if x not in seen_item]:
                        if item not in rank:
                            rank[item]=0
                        rank[item]+=1
                rank=[x[0] for x in sorted(rank.items(),key=lambda x:x[1],reverse=True)[:self.N]]
        else:
            mp=MostPopular(self.data)
            mp.compute_recommendation()
            rank=mp.recommendation[user][:self.N]
        return rank


    def __get_recommendation(self): #recommend for all user
        recs={}
        for user in self.data.users:
            if user not in recs:
                recs[user]=[]
            recs[user]=self.__recommend(user)
        return recs


# In[3]:


# if __name__=='__main__':
#     dt=Data()
#     uf=UserCF(dt)
#     uf.compute_recommendation()
#     for user in dt.old_users:
#         print(user)
#         print(uf.recommendation[user])
#         print('_'*20)

