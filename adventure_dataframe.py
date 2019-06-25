import requests
import urllib.request
import time
import os.path 
from bs4 import BeautifulSoup
import pandas as pd 
from lxml import html
import numpy as np
import re

len_anchors = 280#280

size = len_anchors*2000
eps = ["" for x in range(size)]
lines =  ["" for x in range(size)]
names =  ["" for x in range(size)]
dialogue =  ["" for x in range(size)]
actions =  ["" for x in range(size)]

end_of_last_k = 0 
for i in range(len_anchors):
    if os.path.exists('./transcripts/adventure_time_ep'+str(i)+'_redacted.html'):
        html = open('./transcripts/adventure_time_ep'+str(i)+'_redacted.html','r')
        soup = BeautifulSoup(html, "lxml")
        for script in soup(["script", "style"]):  # kill all script and style elements
            script.extract()    # rip it out
        text = soup.get_text()
        text_by_line = text.split('\n')
        text_no_breaks = [l for l in text_by_line if len(l) > 0]
        num_lines = len(text_no_breaks)
        line_count = 0
        for k in range(num_lines):
            eps[k + end_of_last_k] = i
            lines[k + end_of_last_k] = k
            if len(text_no_breaks[k]) > 1:
                line_count = line_count + 1
                split_up = text_no_breaks[k].split(':',maxsplit=1)
                this_lines_actions = []
                words = []
                if re.match(r'^\W',text_no_breaks[k]):
                    person = 'Narrator'
                    words.append(text_no_breaks[k])
                    this_lines_actions.append(words)
                elif len(split_up) == 2:
                    person = split_up[0]
                else:
                    print("Error in split!",i,k,text_no_breaks[k])
                names[line_count + end_of_last_k] = person
                more_words = []
                if not 'Narrator' in person:
                    split_by_italics = split_up[1].split('[')
                    if len(split_by_italics) > 1:
                        for w in range(len(split_by_italics)): #len > 1 indicates actions are present
                            if ']' in split_by_italics[w]:
                                an_action = split_by_italics[w].split(']') 
                                if len(an_action[0]) > 0:
                                    thing = []
                                    thing.append(an_action[0])
                                    this_lines_actions.append(thing)
                                if len(an_action[1]) > 0:
                                    thing = []
                                    thing.append(an_action[1])
                                    more_words.append(thing)
                            else: 
                                if len(split_by_italics[w]) > 1:
                                    this_thing = []
                                    this_thing.append(split_by_italics[w])
                                    more_words.append(this_thing)
                    elif len(split_by_italics) == 1:
                        more_words.append(split_by_italics)
                if len(more_words) == 1:
                    dialogue[line_count + end_of_last_k] = more_words[0]
                elif len(more_words) > 1:
                    no_spaces = []
                    for y in range(len(more_words)):
                        if len(more_words[y][0]) > 2:
                            no_spaces.append(more_words[y])
                    dialogue[line_count + end_of_last_k] = no_spaces
                if len(this_lines_actions) == 1:
                    actions[line_count + end_of_last_k] = this_lines_actions[0]
                elif len(this_lines_actions) > 1:
                    actions[line_count + end_of_last_k] = this_lines_actions
                #print("character for line ",k,": ",names[line_count + end_of_last_k])
                #print("words for line ",k,": ",dialogue[line_count + end_of_last_k])
                #print("actions for line ",k,": ",actions[line_count + end_of_last_k]) 
                #print("line ",k,": ",names[line_count + end_of_last_k],": ",dialogue[line_count + end_of_last_k],actions[line_count + end_of_last_k])                      
        end_of_last_k = k + end_of_last_k


#### using data constructed above, let's make a dataframe!
eps = eps[:end_of_last_k+1]
eps = np.asarray(eps).T 
lines = lines[:end_of_last_k+1]
lines = np.asarray(lines).T
names = names[:end_of_last_k+1]
dialogue = dialogue[:end_of_last_k+1]
actions = actions[:end_of_last_k+1]
names = np.asarray(names).T 

data = [[None]*5 for i in range(end_of_last_k+1)]
for i in range(len(data)):
    data[i][0] = eps[i]
    data[i][1] = lines[i]
    data[i][2] = names[i]
    if len(dialogue[i]) > 1:
        ## CONCATENATE ELEMENTS OF IT
        s = ', '
        data[i][3] = s.join(["".join(x) for x in dialogue[i]])
    elif len(dialogue[i]) == 1:
        data[i][3] = str(dialogue[i][0])
    elif len(dialogue[i]) == 0:
        data[i][3] = ""
    if len(actions[i]) > 1:
        ## CONCATENATE ELEMENTS OF IT
        s = ', '
        data[i][4] = s.join(["".join(x) for x in actions[i]])
    elif len(actions[i]) == 1:
        data[i][4] = str(actions[i][0])
    elif len(actions[i]) == 0:
        data[i][4] = ""
    data[i] = tuple(data[i])

df = pd.DataFrame(data,columns = ['Episode','Line','Character','Dialogue','Action'])
df['Action'] = df['Action'].str.lower() 
df['Dialogue'] = df['Dialogue'].str.lower() 
df.to_pickle("./adventure_pickle_tupled_2019-06-24.pkl")