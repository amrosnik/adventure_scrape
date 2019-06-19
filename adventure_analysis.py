import requests
import urllib.request
import time
import os.path 
from bs4 import BeautifulSoup
import pandas as pd 
from lxml import html
import numpy as np
import re

#### let's do some analysis on adventure data! ####

df = pd.read_pickle("./adventure_pickle_CLEAN.pkl")
pd.set_option('display.max_rows',None)
pd.set_option('display.max_columns',None)
pd.set_option('display.expand_frame_repr',False)
pd.set_option('max_colwidth',-1)

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
counts = dwords['dialogue word'].value_counts()
print(counts)
print(dwords['dialogue word'].mode())

### TO DO: MAKE PLOTS OR PRETTY TABLES OF WORDS BY COUNTS, if count > 10
### TO DO: save value_counts as a df? so can pick out count > 10? not sure how this works 