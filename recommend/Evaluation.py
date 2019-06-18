
# coding: utf-8

# In[22]:


class Evaluation:
    def __init__(self,recommend_algorithm):
        self.rec_alg=recommend_algorithm  
        
        self.precision=None
        self.recall=None
        self.coverage=None
        self.popularity=None
    
    def evaluate(self):
        self.precision,self.recall=self.__precision_recall()
#         print("准确率= " + str(self.precision)+';'+"召回率= "+str(self.recall))
        
        self.coverage=self.__coverage()
#         print("覆盖率="+str(self.coverage))
        
        self.popularity=self.__popularity()
#         print("流行度="+str(self.popularity))
        
    def __precision_recall(self): 
        hit=0
        len_pred=0
        len_true=0
        for user in self.rec_alg.data.test_dic:
            pred_list=self.rec_alg.recommendation[user]
            len_pred+=len(pred_list)
            if user in self.rec_alg.data.dic:
                if 0 in self.rec_alg.data.dic[user]:
                    true_list=self.rec_alg.data.dic[user][0]
                else:true_list=[]
            else:true_list=[]
            len_true+=len(true_list)
            for item in true_list:
                if item in pred_list:
                    hit+=1
        return hit*100/len_pred,hit*100/len_true

    
    def __coverage(self):
        #coverage=len(rec_pred)/len(items)
        rec_pred=set()
        for user in self.rec_alg.data.test_dic:
            pred_item=self.rec_alg.recommendation[user]
            for item in pred_item:
                rec_pred.add(item)
        return len(rec_pred)*100/len(self.rec_alg.data.items)
    
    def __popularity(self):
        #popularity=pop(rec_pred)/count
        pop_sum=0.0
        count=0.0
        for user in self.rec_alg.data.test_dic:
            rec_items=self.rec_alg.recommendation[user]
            for item in rec_items:
                if item in self.rec_alg.data.item_pop:
                    pop_sum+=self.rec_alg.data.item_pop[item]
                    count+=1
                else:continue
        if pop_sum==0 or count==0:return 0
        return pop_sum/count


# In[23]:


# from Data import Data
# from MostPopular import MostPopular
# from UserCF import UserCF
# from ItemCF import ItemCF
# import numpy as np

# if __name__=='__main__':
#     dt=Data()
    
#     clfs=[MostPopular,UserCF,ItemCF]
#     for i in range(3):
#         clf=clfs[i]
        
#         precisions=[]
#         recalls=[]
#         coverages=[]
#         popularities=[]
        
#         recommend=clf(dt)
#         recommend.compute_recommendation()
#         eva=Evaluation(recommend)
#         eva.evaluate()
        
#         precisions.append(eva.precision)
#         recalls.append(eva.recall)
#         coverages.append(eva.coverage)
#         popularities.append(eva.popularity)
#         print('-'*20)
#         print(clf.__name__)
#         print("Avg Precision:",np.mean(precisions))
#         print("Avg Recall:",np.mean(recalls))
#         print("Avg Coverage:",np.mean(coverages))
#         print("Avg Popularity:",np.mean(popularities)) 
#         print('_'*20)

