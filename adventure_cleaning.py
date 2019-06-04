import requests
import urllib.request
import time
import os.path 
from bs4 import BeautifulSoup
import pandas as pd 
from lxml import html
import numpy as np
import re

df = pd.read_pickle("./adventure_pickle.pkl")
pd.set_option('display.max_rows',None)
pd.set_option('display.max_columns',None)
pd.set_option('display.expand_frame_repr',False)
pd.set_option('max_colwidth',-1)

#file = open("character.test",'w')
#file.write(str(df.groupby(df['Character'].str.lower()).count()))
#file.close()

#print(df.groupby('Character').count())
#print(df.loc[df['Character'] == 'Finn'].count())
#print(df.loc[df['Character'] == 'Princess Bubblegum'].count())
#print(len(df.loc[df['Character'] == 'Princess Bubblegum']))

#### FUNCTIONS FOR CLEANING DATA ####
def combine_names(ex1,ex2):
    ### combine rows w/ Character attributes of ex1 and ex2
    ### need to do a combo of groupby, aggregate, and (outer) join @_@ 
    ### groupby['Character'], then aggregate 

## Beemo, BMO
## Betty, Betty Grof? 
## Both Finn and Jake,Both Finn and Jake, Finn & Jake [X], Finn and Jake [X], Jake and Finn
## Bubblegum, Princess Bubblegum, Princes Bubblegum, Princess Bubblgum, Princess Bubblegun, Princess Bubblegum [X]..also, Bonnie?
## Candy Person [X], Candy Sheriff, Candy Tavern Person, Candy children, Candy crowd,
## (cont.) Candy dude, Candy person, Candy soldier, Candy soldiers, Random candy person
## Candy butler and Peppermint butler?????
## Chery Cream Soda, Cherry Cream Soda
## Demon in crowd, Demon in crowd #2, Demon in line
## Dream Jake, Dream Jake (slowly)
## Fat Villager [x]
## Finn [x]
## CharacterX, CharacterX [flashback]
## Finn & Princess Bubblegum, Finn and Princess Bubblegum
## Finn's Mother, Finn's mom
## Flame Guard [x]
## Flame People, Flame Person
## Flame Princess [x]
## Flying Banana Guard, Flying Banana Guards
## Flying Lettuce Brother, Flying Lettuce Brothers
## Fox [X]
## Gnome [X]
## Goblin Thief [X]
## Guard [X]
## Gumball Guardian [X]
## Gumdrop Lass [X], Gumdrop Lasses
## Gunter, Gunther
## Head Marauder
## Hot Dog Night [X]
## Hooligan, Hooligans
## Hunson, Hunson Abadeer
## Ice Kin [X]
## King of Ooo, King Of Ooo
## Lady, Lady Rainicorn
## Lady and Finn; Lady, Finn
## Lesser Flame Guard [X], Lesser Flame Guards
## Lollipop Girl, Lollipop girl
## Lumpy Space Princess [x]
## Magic Man, Magic Man [quietly]
## Marauder [X]
## Marcelince, Marceline, Marc, Marcy 
## Marshmallow Kid [X], Marshmallow Kids
## Mr. Pig & Tree Trunks, Mr. Pig and Tree Trunks
## Muscular Ghost [X]
## Nymph, Nymphs
## Penguin, Penguins
## Professor Worm, Professor worm
## Royal Tart Path Guard [X]
## Simon [X]
## Snail Lady [x]
## Soft Person X (same as pillow ppl???)
## Spiky Guard, (s)
## Starchie, Starchie (on radio), Starchy
## Suitor [x]
## Susan, Susan Strong
## Syrup Guard [x]
## T.V., TV
## Lich, The Lich
## [ all the banana guards, if not prev. mentioned]
## Townsperson, Townspeople [X]
## Tree Trunks
## Tree Witch, Tree Witch'
## Wildberry Guard [x]
## Wildberry kid,(S)
## Worker,(s)
## [double-check if different-colored BMO's are actually BMO's or other MO's]