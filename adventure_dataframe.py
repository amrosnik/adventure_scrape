import requests
import urllib.request
import time
import os.path 
from bs4 import BeautifulSoup
import pandas as pd 
import numpy as np

len_anchors = 280

eps = np.zeros(len_anchors*2000)
lines = np.zeros(len_anchors*2000)
names = np.zeros(len_anchors*2000)
dialogue = np.zeros(len_anchors*2000)
actions = np.zeros(len_anchors*2000)

end_of_last_k = 0 
for i in range(len_anchors):
    if os.path.exists('adventure_time_ep'+str(i)+'_redacted.html'):
        html_script = open('adventure_time_ep'+str(i)+'_redacted.html','r')
        print("****************************")
        num_lines = sum(1 for line in html_script if len(line) > 1)
        for k in range(num_lines):
            eps[k + end_of_last_k] = i
            lines[k + end_of_last_k] = k
            #print(eps[k + end_of_last_k],k + end_of_last_k)
        line_count = 0 
        for f in html_script:
            if len(f) > 1:
                line_count = line_count + 1
                f_ended = f[:-1]
                #print(f[:-1]) #need to exclude last character, as it somehow is another line/a large space 
                #print(len(f.split('</b>:')))
                split_up = f_ended.split('</b>:')
                if len(split_up) == 1:
                    person = 'Narrator'
                    words = split_up[0]
                elif len(split_up) == 2:
                    person = split_up[0]
                    words = split_up[1]
                else:
                    print("Error in split!")
                names[line_count + end_of_last_k] = person
                dialogue[line_count + end_of_last_k] = words
        end_of_last_k = k + end_of_last_k
        html_script.close()
                ## column 2: f[0] w/o <b> tags, colon 
                ## column 3:  



        #ep_dataframe = pd.Dataframe()
