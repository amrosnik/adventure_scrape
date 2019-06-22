import requests
import urllib.request
import time
import os.path 
import pandas as pd 
import numpy as np
import re

df = pd.read_pickle("./adventure_pickle_CLEAN.pkl")
pd.set_option('display.max_rows',None)
pd.set_option('display.max_columns',None)
pd.set_option('display.expand_frame_repr',False)
pd.set_option('max_colwidth',-1)

df = df.loc[df['Episode'].str.len() > 0]
df['Episode'] = df['Episode'].astype('int64',copy=False)
df['Line'] = df['Line'].astype('int64',copy=False)
df.sort_values(by=['Episode','Line'],inplace=True)

finn_df = df.loc[df['Character'] == 'finn']

finn_df.to_pickle("./finn_pickle.pkl")