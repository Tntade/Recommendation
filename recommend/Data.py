
# coding: utf-8

# In[9]:


import numpy as np
import pandas as pd
import random
from sklearn.cross_validation import train_test_split


class Data:
    
    def __init__(self):
        
        self.old_users=['C2002002', 'C2011020', 'C2016004', 'C2016005', 'C2012003', 'C2016003', 'C2012011', 'C1001001', 
          'C2016014', 'C2018002', 'C2012001', 'C2012002', 'C2002007', 'C2003001', 'C2000007', 'C2016009', 
          'C2028001', 'C2002010', 'C2017001', 'C2001002', 'C2019001', 'C2002008', 'C2011021',
          'C2012004', 'C1007002', 'C2018001', 'C2004003']
        
        self.data=self.__get_data()
        
        tmp=self.data[['user','item']].values
        self.users=set() #users=old_users+new_users
        self.items=set() #items=old_items+new_items(buy and quote)
        for i in range(len(tmp)):
            user=tmp[i][0]
            item=tmp[i][1]
            self.users.add(user)
            self.items.add(item)
        
        self.new_users=[x for x in self.users if x not in self.old_users]
        
        self.newdf,self.train,self.test=self.__split_data()

        self.dic,self.test_dic=self.__convert_dic() #train_dic,test_dic
        
        self.train_users=set()
        self.train_items=set()
        temp=self.train[['user','item']].values
        for i in range(len(temp)):
            user=temp[i][0]
            item=temp[i][1]
            self.train_users.add(user)
            self.train_items.add(item)
        
        self.user_industry=self.__user_industry() #user_industry={user:ind,user:ind,.....}
        self.item_pop=self.__item_pop()    
    
    def __get_data(self): 
        #在这里做了简单的打标签的特征工程，如果特征工程作的比较多，可以另外放一个类中进行调用即可
        df=pd.read_csv('E:\\Python2Projects_LOCAL\\yf_data\\yufang0508.csv')
        for col in ['item','industry']:
            df[col]=df[col].astype(str)
        df['item_len']=df['item'].apply(lambda x:int(len(x)))
        df['item_label_1']=0
        df['item_label_2']=0
        df.loc[df['item_len']==6,'item_label_1']=df['item'].apply(lambda x:str(x)[:1])
        df.loc[df['item_len']==7,'item_label_1']=df['item'].apply(lambda x:str(x)[:2])
        df.loc[df['item_len']==6,'item_label_2']=df['item'].apply(lambda x:str(x)[1:3])
        df.loc[df['item_len']==7,'item_label_2']=df['item'].apply(lambda x:str(x)[2:4])
        df['industry_str']='idx_'+df['industry']
        df=df.drop(['item_len'],axis=1)
        return df            

    #根据最新调整的版本，如果是新用户，直接根据MostPopular进行推荐，然后在老用户中随机分成train+test二个部分
    def __split_data(self):
        new=[]
        old=[]
        tmp=self.data.values
        header=self.data.columns.tolist()
        for i in range(len(tmp)):
            if tmp[i][0] in self.new_users:
                new.append(tmp[i])
            else:
                old.append(tmp[i])
#         print("new_user samples len:",len(new))
#         print("old_user samples len:",len(old))
        new_data=pd.DataFrame(new,columns=header)
        old_data=pd.DataFrame(old,columns=header)
        
        seed=random.randint(0,2019)
        train,test=train_test_split(old_data,test_size=0.2,random_state=seed)
#         print("train samples len:",len(train))
#         print("test samples len:",len(test))
        
        return new_data,train,test #return:新用户df,traindf,testdf
    
    def __convert_dic(self):
        tmp_train=self.train[['user','is_quote','item']].values
        tmp_test=self.test[['user','is_quote','item']].values
        def get_dic(tmp):
            d={}
            for i in range(len(tmp)):
                user=tmp[i][0]
                is_quote=tmp[i][1]
                item=tmp[i][2]
                if user not in d:
                    d[user]={}
                if is_quote not in d[user]:
                    d[user][is_quote]=[]
                if item not in d[user][is_quote]:
                    d[user][is_quote].append(item) 
            return d    #return:#{user:{0:[1,2,3],1:[3,4,5]}} ,0代表购买的item,1代表询价的item  
        return get_dic(tmp_train),get_dic(tmp_test)
    
    
    def __user_industry(self): #由于user_ind是可以得到的，所以可以将所有用户放到一起得到dic
        user_industry={}
        tmp=self.data[['user','industry']].values
        for i in range(len(tmp)):
            user=tmp[i][0]
            ind=tmp[i][1]
            if user not in user_industry:
                user_industry[user]=0
            user_industry[user]=ind
        return user_industry
    
    def __item_pop(self):
        item_pop={}
        tmp=self.data[['is_quote','item']].values
        for i in range(len(tmp)):
            is_quote=tmp[i][0]
            item=tmp[i][1]
            if is_quote==0:
                if item not in item_pop:
                    item_pop[item]=0
                item_pop[item]+=1
            elif is_quote==1:
                if item not in item_pop:
                    item_pop[item]=0
                item_pop[item]+=0.5
        return item_pop


