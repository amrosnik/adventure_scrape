import requests
import urllib.request
import time
import os.path 
import pandas as pd 
import numpy as np
import re
import adventure_analysis 
import pickle

df = pd.read_pickle("./finn_pickle.pkl")

df['Dialogue'] = df['Dialogue'].str.lower().str.replace("'","")
df['Dialogue'] = df['Dialogue'].str.lower().str.replace("[","")
df['Dialogue'] = df['Dialogue'].str.lower().str.replace("]","")
df['Dialogue'] = df['Dialogue'].str.lower().str.replace("\t"," ")
df['dialogue words'] = df.loc[:,'Dialogue'].str.strip().str.split('[\s_\-\'.:;)(!?,"\[\]]+')
df['Action'] = df['Action'].str.lower() 
df['action words'] = df.loc[:,'Action'].str.strip().str.split('[\s_:;\-\')(.!?,"\[\]]+')

#print(df.head())
dwords,awords = adventure_analysis.word_by_word(df)

counts,word_sum,c_d,idf,tf_idf = adventure_analysis.calc_mining_stats(dwords)
tf_idf.sort_index(by='tf_idf',inplace=True)
tf_idf.sort_values(by='tf_idf',ascending=True,inplace=True)
#print(tf_idf.tail())
## need to one-hot encode finn data
### first: strip it to just dialogue 
pre_one_hot = df['Dialogue'].to_list() ## or dialogue words? 
print(pre_one_hot)
with open('./finn_just_dialogue.pkl', 'wb') as fp:
    pickle.dump(pre_one_hot, fp)