import requests
import urllib.request
import time
import os.path 
from bs4 import BeautifulSoup
import pandas as pd 
from lxml import html
import numpy as np
import re

df = pd.read_pickle("./adventure_pickle_tupled.pkl")
pd.set_option('display.max_rows',None)
pd.set_option('display.max_columns',None)
pd.set_option('display.expand_frame_repr',False)
pd.set_option('max_colwidth',-1)

df['Character'] = df['Character'].str.lower() 
grpd = df.groupby('Character')

#file = open("character_list.out",'w')
#file.write(str(grpd.count()))
#file.close()

#### FUNCTIONS FOR CLEANING DATA ####
def combine_names(ex1,ex2,which_name):
    ### combine rows w/ Character attributes of ex1 and ex2 (these args are strings)
    new_df = pd.concat([df.loc[df['Character'] == ex1],df.loc[df['Character'] == ex2]])
    if which_name == 1:
        new_df.loc[new_df['Character'] == ex2, 'Character'] = ex1
    elif which_name == 2:
        new_df.loc[new_df['Character'] == ex1, 'Character'] = ex2
    else:
        print("Improper which_name value! Must be 1 or 2.")
    return new_df

def combine_names_in_list(list_of_grps,which_name):
    list_of_dfs = [df.loc[df['Character'] == x] for x in list_of_grps]
    new_df = pd.concat(list_of_dfs)
    limit_which_name = len(list_of_grps)
    if which_name <= limit_which_name: 
        for i in range(limit_which_name):
            new_df.loc[new_df['Character'] == list_of_grps[i], 'Character'] = list_of_grps[which_name]
    else:
        print("Improper which_name value!")
    return new_df

banana_list = ['banana guard','another banana guard', 'captain banana guard', 'female banana guard', 'private banana guard','the four banana guards','banana guards','banana guard #1','banana guard #2','banana guard (on radio)','banana guard 500',"banana guard [in finn's memory]",'banana guard [over phone]','banana guard i','banana guard ii','banana guard leader','banana guard number 3','flying banana guard', 'flying banana guards']
banana_df = combine_names_in_list(banana_list,0)

#voice_list = ['a voice','a voice in the distance']
#voice_df = combine_names_in_list(voice_list,0)

#alarm_list = ['alarm','alarm clock bird','alarm clock with a headshot of princess bubblegum taped to the minute hand']
#alarm_df = combine_names_in_list(alarm_list,0)

#alien_list = ['alien groom','aliens']
#alien_df = combine_names_in_list(alien_list,0)

#townppl_list = ['townspeople (all)','townsperson','villager','villager with eyepatch','townsperson (blue shirt)','townsperson (green shirt)','townsperson (red shirt)','townsperson with fire-spitting belly button']
#townppl_df = combine_names_in_list(townppl_list,1)

#syrup_guard_list = ['syrup guard','syrup guard #2','syrup guard #3','syrup guard #4']
#syrup_df = combine_names_in_list(syrup_guard_list,0)

susan_list = ['susan','susan strong']
susan_df = combine_names_in_list(susan_list,1)

#softppl_list = ['soft people','soft child','fluffy person','soft person #1','soft person #2', 'soft person #3','old soft person']
#softppl_df = combine_names_in_list(softppl_list,0)

#smo_list = ['smo 1','smo 2','smo 3','smo 4','smo 5','smo 6']
#smo_df = combine_names_in_list(smo_list,0)

#snail_lady_list = ['snail lady','snail ladies','snail lady #1','snail lady #2','snail lady #3','snail lady #4']
#snail_lady_df = combine_names_in_list(snail_lady_list,0)

#tart_guard_list = ['royal tart path guard 1','royal tart path guard 2','royal tart path guard 3','royal tart path guard 4','royal tart path guard 5','royal tart path guard 6','royal tart path guard 7','royal tart path guard 8']
#tart_guard_df = combine_names_in_list(tart_guard_list,0)

#pillow_list = ['pillow people','pillow child','pillow children']
#pillow_df = combine_names_in_list(pillow_list,0)

#penguin_list = ['penguin','penguin [on tape]','penguins','gunthalina']
#penguin_df = combine_names_in_list(penguin_list,0)

magic_man_list = ['magic man','magic man [as jake]','magic man [quietly]']
magic_man_df = combine_names_in_list(magic_man_list,0)

#lesser_flame_guard_list = ['lesser flame guards','lesser flame guard 1','lesser flame guard 2','lesser flame guard 3']
#lesser_flame_guard_df = combine_names_in_list(lesser_flame_guard_list,0)


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
## Spiky Guard, (s)
## Starchie, Starchie (on radio), Starchy
## Suitor [x]
## Susan, Susan Strong
## T.V., TV
## Lich, The Lich
## Tree Trunks
## Tree Witch, Tree Witch'
## Wildberry Guard [x]
## Wildberry kid,(S)
## Worker,(s)
## [double-check if different-colored BMO's are actually BMO's or other MO's]