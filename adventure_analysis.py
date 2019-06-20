import requests
import urllib.request
import time
import os.path 
import pandas as pd 
import numpy as np
import re
import matplotlib.pyplot as plt 

#### let's do some analysis on adventure data! ####

idx = pd.IndexSlice
df = pd.read_pickle("./adventure_pickle_CLEAN.pkl")
pd.set_option('display.max_rows',None)
pd.set_option('display.max_columns',None)
pd.set_option('display.expand_frame_repr',False)
pd.set_option('max_colwidth',-1)

df = df.loc[df['Episode'].str.len() > 0]
df['Episode'] = df['Episode'].astype('int64',copy=False)
df['Line'] = df['Line'].astype('int64',copy=False)
df.sort_values(by=['Episode','Line'],inplace=True)
#print(df.head())

test_marceline = df.loc[df['Character'] == 'marceline']
test_pb = df.loc[df['Character'] == 'princess bubblegum']

def word_by_word(data):
    data['Dialogue'] = data['Dialogue'].str.lower() 
    data['dialogue words'] = data.loc[:,'Dialogue'].str.strip().str.split('[\s_.:;)(!?,"\[\]]+')
    data['Action'] = data['Action'].str.lower() 
    data['action words'] = data.loc[:,'Action'].str.strip().str.split('[\s_:;)(.!?,"\[\]]+')

    drows = list()
    for row in data[['Episode','Line','Character', 'dialogue words']].iterrows():
        r = row[1]
        for word in r['dialogue words']:
            drows.append((r['Episode'], r['Line'], r['Character'], word))

    dwords = pd.DataFrame(drows, columns=['Episode','Line','Character', 'dialogue word'])
    dwords = dwords[dwords['dialogue word'].str.len() > 0]
    dwords = dwords[dwords['dialogue word'] != '\'']

    arows = list()
    for row in data[['Episode','Line','Character', 'action words']].iterrows():
        r = row[1]
        for word in r['action words']:
            arows.append((r['Episode'], r['Line'], r['Character'], word))

    awords = pd.DataFrame(arows, columns=['Episode','Line','Character', 'action word'])
    awords = awords[awords['action word'].str.len() > 0]
    awords = awords[awords['action word'] != '\'']

    return dwords,awords

dwords,awords = word_by_word(test_marceline)
dwords,awords = word_by_word(test_pb)
#print(dwords.head())

counts = dwords.groupby('Episode')['dialogue word'].value_counts().to_frame().rename(columns={'dialogue word':'n_w'})

def pretty_plot_top_n(series,k,file_name,top_n=5, index_level=0):
    r = series.groupby(level=index_level).nlargest(top_n).reset_index(level=index_level,drop=True)
    #slice_r = r[r['Episode'] < 100]
    plt.figure(figsize=(15,9))
    plt.tight_layout()
    r.plot(kind='bar',y='n_w')
    plt.xticks(fontsize=10)
    #plt.show()
    plt.savefig(file_name+'_set'+str(k)+'.png')
    return r.to_frame()


end_num = [((i+1)*15 + 1) for i in range(20)]
start_num = [i*15 for i in range(20)]
#for k in range(len(start_num)):
#    print(start_num[k],end_num[k])
#    set_k = counts.loc[idx[start_num[k]:end_num[k],:]]
#    if len(set_k) > 0:
#        pretty_plot_top_n(set_k['n_w'],k,'counts_pb',top_n=10)

word_sum = counts.groupby(level=0).sum().rename(columns={'n_w':'n_d'})

tf = counts.join(word_sum)
tf['tf'] = tf['n_w']/tf['n_d']

c_d = dwords['Episode'].nunique()
idf = dwords.groupby('dialogue word')['Episode'].nunique().to_frame().rename(columns={'Episode':'i_d'}).sort_values('i_d')
idf['idf'] = np.log(c_d/idf['i_d'].values)
tf_idf = tf.join(idf)
tf_idf['tf_idf'] = tf_idf['tf'] * tf_idf['idf']
#print(tf_idf['tf_idf'])
#tf_idf.sort_index(by='tf_idf',inplace=True)
#tf_idf.sort_values(by='tf_idf',ascending=True,inplace=True)
#print(tf_idf.loc[idx[0:10,'tf_idf']].sort_values(ascending=True,inplace=True))
    #.sort_values(by='tf_idf',ascending=True,inplace=True))
#print(tf_idf.head())

#for k in range(len(start_num)):
#    print(start_num[k],end_num[k])
#    set_k = tf_idf.loc[idx[start_num[k]:end_num[k],:]]
#    if len(set_k) > 0:
#        pretty_plot_top_n(set_k['tf_idf'],k,'tf-idf_pb',top_n=5)



### can we track words by 'dialogue words' index to see how their tf-idf changes with episode? 
### game plan: 
#### 1.switch levels in tf_idf 
#### 2. 
words = tf_idf.index.get_level_values(level=1).unique().tolist()
#for word in words:
get_more = tf_idf.swaplevel(i=0, j=1, axis=0)
get_more.unstack()
get_more.reset_index(level=1, inplace=True)
#print(get_more.groupby('Episode').count())
print(get_more[get_more.index.str.equals('the')]) ## this doesn't work 
#print(get_more.head())
#workin_with = tf_idf.unstack()
    #workin_with = tf_idf.loc[tf_idf['dialogue words'] == word]
#print(workin_with)