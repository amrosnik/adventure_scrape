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

#print(df.loc[df['Character'] == 'princess bubblegum','Episode'].mode())

### possible process for breaking down each row into words...

# for every place in df where 'Character' == princess bubblegum: 
# split 'Dialogue' and 'Action' by spaces, punctuation, tabs into single words 
# if not 'the','an','a','and','or','&',' ':
    # save mini arrays: Character Episode Line Dialogue_word Action_word 

#print(df['Character'].value_counts())

test_marceline = df.loc[df['Character'] == 'marceline']
test_marceline['Dialogue'] = test_marceline['Dialogue'].str.lower() 
test_marceline['dialogue words'] = test_marceline.loc[:,'Dialogue'].str.strip().str.split('[\s_]+')
test_marceline['Action'] = test_marceline['Action'].str.lower() 
test_marceline['action words'] = test_marceline.loc[:,'Action'].str.strip().str.split('[\s_]+')
#test_marceline['action words'] = test_marceline['action words'].str.replace(',','')
print(test_marceline.head())

#word_by_word 
#for i in range(len(test_marceline)):
    