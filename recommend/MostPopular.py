
# coding: utf-8

# In[7]:

#实际上是MostPopularNewUser
class MostPopular:  
    def __init__(self,data):
        self.data=data 
        
        self.ind_item_pop=self.__industry_item_pop() 

        self.N=None
        self.recommendation=None
    
    def compute_recommendation(self,N=5):  
        self.N=N
        self.recommendation=self.__get_recommendation() 
    
    def __industry_item_pop(self):
        ddic={}
        tmp=self.data.train
        tmp=tmp[['user','is_quote','item']].values
        for i in range(len(tmp)):
            u=tmp[i][0]
            u_ind=self.data.user_industry[u]
            if u_ind not in ddic:
                ddic[u_ind]={}
            quote=tmp[i][1]
            item=tmp[i][2]
            if item not in ddic[u_ind]:
                ddic[u_ind][item]=0
            ddic[u_ind][item]=self.data.item_pop[item]
        ddic={u:sorted(v.items(),key=lambda x:x[1],reverse=True) for u,v in ddic.items()}
        return ddic

    def __recommend(self,user):
        user_ind=self.data.user_industry[user]
        industry_ranked_items=[x[0] for x in self.ind_item_pop[user_ind]]
        if user in self.data.new_users:  
            rank=[x for x in industry_ranked_items][:self.N]
        else:
            if user in self.data.dic:
                if 0 in self.data.dic[user]:
                    seen_item=self.data.dic[user][0]
                else:seen_item=[]
            else:
                seen_item=[]
            rank=[x for x in industry_ranked_items if x not in seen_item][self.N]
        return rank
    
    def __get_recommendation(self):
        recs={}    
        for user in self.data.users:
            if user not in recs:
                recs[user]=[]
            recs[user]=self.__recommend(user)
        return recs 


# In[8]:


# from Data import Data

# if __name__=='__main__':
#     data=Data()
#     new_user=data.new_users
    
#     mp=MostPopular(data)
#     mp.compute_recommendation()

