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
        #url = "http://news.bbc.co.uk/2/hi/health/2284783.stm"
        #html = urllib.urlopen(url).read()
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
                #f_ended = f[:-1]
                #print(f[:-1]) #need to exclude last character, as it somehow is another line/a large space 
                split_up = text_no_breaks[k].split(':',maxsplit=1)
                this_lines_actions = []
                words = []
                #if len(split_up) == 1:
                if re.match(r'^\W',text_no_breaks[k]):
                    person = 'Narrator'
                    #print(text_no_breaks[k])
                    #words.append(split_up[0])
                    words.append(text_no_breaks[k])
                    this_lines_actions.append(words)
                    #actions[line_count + end_of_last_k] = words
                    #print(person,line_count)
                elif len(split_up) == 2:
                    person = split_up[0]
                else:
                    print("Error in split!",i,k,text_no_breaks[k])
                names[line_count + end_of_last_k] = person
                more_words = []
                if not 'Narrator' in person:
                    split_by_italics = split_up[1].split('[')
                    #print(len(split_by_italics),split_by_italics)
                    if len(split_by_italics) > 1:
                        for w in range(len(split_by_italics)): #len > 1 indicates actions are present
                            if ']' in split_by_italics[w]:
                                an_action = split_by_italics[w].split(']') 
                                #print(k,w,an_action)
                                if len(an_action[0]) > 0:
                                    #print(an_action[0])
                                    thing = []
                                    thing.append(an_action[0])
                                    this_lines_actions.append(thing)
                                if len(an_action[1]) > 0:
                                    #print(an_action[1])
                                    thing = []
                                    thing.append(an_action[1])
                                    #print(more_words)
                                    #print(len(an_action[1]),an_action[1])
                                    more_words.append(thing)
                                    #print(more_words)
                            else: 
                                if len(split_by_italics[w]) > 1:
                                    #print(len(split_by_italics[w]),split_by_italics[w])
                                    this_thing = []
                                    this_thing.append(split_by_italics[w])
                                    more_words.append(this_thing)
                                    #print(more_words)
                    elif len(split_by_italics) == 1:
                        #print(i,k,split_by_italics)
                        more_words.append(split_by_italics)
                if len(more_words) == 1:
                    #print(more_words)
                    dialogue[line_count + end_of_last_k] = more_words[0]
                elif len(more_words) > 1:
                    no_spaces = []
                    for y in range(len(more_words)):
                        if len(more_words[y][0]) > 2:
                            #print(i,k,y)
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

#for l in range(len(dialogue)):
#    if len(dialogue[l]) > 3:
#        print(len(dialogue[l]),dialogue[l])
#for l in range(len(actions)):
#    print(len(actions[l]),actions[l])

data = [[None]*5 for i in range(end_of_last_k+1)]
for i in range(len(data)):
    data[i][0] = eps[i]
    data[i][1] = lines[i]
    data[i][2] = names[i]
    if len(dialogue[i]) > 1:
        ## INSTEAD: CONCATENATE ELEMENTS OF IT
        #data[i][3] = tuple(dialogue[i])
        s = ', '
        data[i][3] = s.join(["".join(x) for x in dialogue[i]])
        #print(data[i][3])
    elif len(dialogue[i]) == 1:
        #data[i][3] = dialogue[i][0]
        data[i][3] = str(dialogue[i][0])
    elif len(dialogue[i]) == 0:
        data[i][3] = ""
    if len(actions[i]) > 1:
        ## INSTEAD: CONCATENATE ELEMENTS OF IT
        #data[i][4] = tuple(actions[i])
        s = ', '
        data[i][4] = s.join(["".join(x) for x in actions[i]])
        #print(data[i][4])
    elif len(actions[i]) == 1:
        #data[i][4] = actions[i][0]
        data[i][4] = str(actions[i][0])
    elif len(actions[i]) == 0:
        data[i][4] = ""
    #print(len(dialogue[i]),len(actions[i]))
    #data[i][0] = tuple(eps[i])
    #data[i][1] = tuple(lines[i])
    #data[i][2] = tuple(names[i])
    #data[i][3] = tuple(dialogue[i])
    #data[i][4] = tuple(actions[i])
    data[i] = tuple(data[i])
    #print(i,len(data[i]))
#print(len(data))
print(data[219])
df = pd.DataFrame(data,columns = ['Episode','Line','Character','Dialogue','Action'])
#print(df.dtypes)
df.to_pickle("./adventure_pickle_tupled.pkl")