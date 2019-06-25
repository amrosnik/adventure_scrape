import requests
import urllib.request
import time
from bs4 import BeautifulSoup

url = 'https://adventuretime.fandom.com/wiki/Category_talk:Transcripts'
response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

anchors = [a for a in (td.find('a') for td in soup.findAll('td')) if a]
anchors = anchors[2:] ## first two results are irrelevant

### i have 213 partial to full transcripts to work with...out of possibly 283 :/ 
for i in range(0,len(anchors)):
    if anchors[i].has_attr('href'):
        link = anchors[i]['href']
        actual_link = 'https://adventuretime.fandom.com'+link 
        file_name = './transcripts/adventure_time_ep'+str(i)+'.html'
        urllib.request.urlretrieve(actual_link,file_name)
        file = open(file_name,'r')
        new_file = [n.replace('<dl><dd>','') for n in file.readlines() if n.startswith('<dl')]
        file.close()
        new_name = open('./transcripts/adventure_time_ep'+str(i)+'_redacted.html','w')
        for k in range(len(new_file)):
            new_name.write(new_file[k]+'\n')
        new_name.close() 
    time.sleep(1)
