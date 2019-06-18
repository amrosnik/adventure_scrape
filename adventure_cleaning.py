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

cake_list = ['cake','fionna and cake']
cake_df = combine_names_in_list(cake_list,0)

tiffany_list =  ['tiffany', 'tiffany and jake','tiffany, gareth and the flying lettuce brothers']
tiffany_df = combine_names_in_list(tiffany_list,0)

fern_list = ['fern','finn & fern']
fern_df = combine_names_in_list(fern_list,0)

gunter_list = ['gunter','gunther']
gunter_df = combine_names_in_list(gunter_list,0)

flame_princess_list = ['flame princess']  ## there are multiple rows with this key, after making case insensitive
flame_princess_df = combine_names_in_list(flame_princess_list,0)

king_ooo_list = ['king of ooo','king of ooo & toronto']
king_ooo_df = combine_names_in_list(king_ooo_list,0)

lady_list = ['lady rainicorn','lady','lady and finn','lady, finn','finn, lady','princess and lady']
lady_df = combine_names_in_list(lady_list,0)

pbutler_list = ['peppermint butler', "peppermint butler's mouth"]
pbutler_df = combine_names_in_list(pbutler_list,0)

simon_list = ['simon','simon (over telephone)','simon [on tape]','simon petrikov','simon/marcy']
simon_df = combine_names_in_list(simon_list,0)

marshall_list = ['marshall lee','marhsall lee']
marshall_df = combine_names_in_list(marshall_list,0)

starchie_list = ['starchie','starchie (on radio)','starchy']
starchie_df = combine_names_in_list(starchie_list,0)

joshua_list = ['joshua','joshua [on tape]','joshua [on tapes, which are being tampered with by jake]','imaginary joshua']
joshua_df = combine_names_in_list(joshua_list,0)

tree_trunks_list = ['tree trunks']  ## there are multiple rows with this key, after making case insensitive
tree_trunks_df = combine_names_in_list(tree_trunks_list,0)

bmo_list = ['bmo','beemo','bmo (flashback)','bmo (os)','bmo (vo)','bmo [as bebe]','bmo [as lorraine]','bmo [as officer davis]','bmo [as ronnie, deeper voice]','bmo [as ronnie]','bmo [flashback]','bmo [in its thoughts]','bmo [narrating]','bmo & bubble']
bmo_df = combine_names_in_list(bmo_list,0)

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

lemongrabs_list = ['lemongrabs','lemongrab 3','lemon camel','lemon children','lemon person','lemon head','orange lemon child','three-pronged lemon child']
lemongrabs_df = combine_names_in_list(lemongrabs_list,0)

lemongrab_list = ['lemongrab','earl of lemongrab']
lemongrab_df = combine_names_in_list(lemongrabs_list,0)

other_lemongrab_list = ['lemongrab 2','lemongrab clone']
other_lemongrab_df = combine_names_in_list(other_lemongrab_list,0)

ice_king_list = ['ice king','ice king [flashback]','ice king [in flashback]','ice king [off-screen]','ice king [on tape]','ice king [voice-over]',"ice king's crown",'ice king & abracadaniel','ice king & marceline','ice king and abracadaniel']
ice_king_df = combine_names_in_list(ice_king_list,0)

lich_list = ['the lich','lich','snail [the lich]', 'lich/jake','lich/sweet p'] 
lich_df = combine_names_in_list(lich_list,0)

prince_gumball_df = df.loc[df['Character'] == 'prince gumball'] 

normal_man_df = df.loc[df['Character'] == 'normal man']

lemonhope_df = df.loc[df['Character'] == 'lemonhope']

fionna_df = df.loc[df['Character'] == 'fionna']

cinnabun_df = df.loc[df['Character'] == 'cinnamon bun']

death_df = df.loc[df['Character'] == 'death']

sweetp_df = df.loc[df['Character'] == 'sweet p']

football_df = df.loc[df['Character'] == 'football']

lsp_list = ['lumpy space princess','lumpy space princess [voice-over]','lsp','lumpy space princess & marceline']
lsp_df = combine_names_in_list(lsp_list,2)

betty_list = ['betty','betty grof']
betty_df = combine_names_in_list(betty_list,0)

hunson_list = ['hunson','hunson abadeer','lord of evil']
hunson_df = combine_names_in_list(hunson_list,1)

finn_list = ['finn','finn & bear','finn (in flashback)','finn (voiceover)','finn [back to normal]','finn [flashback]','finn [fully transformed]',"finn [in finn's thoughts]",'finn [in flashback]',"finn [on bmo's camera]",'finn [on phone]','finn [on voicemail]','finn [voice-over]','finn [whispering still]','future finn','little finn','past finn','transparent finn']
finn_df = combine_names_in_list(finn_list,0)

finn_and_jake_list = ['finn & jake','finn & jake','finn & jake [in unison]','finn & jake [on voicemail]','finn & jake','finn and jake','finn and jake [in unision]','finn and jake [in unison]','finn and jake together','imaginary finn & jake','jake and finn','both finn and jake','both finn and jake'] 
finn_and_jake_df = combine_names_in_list(finn_and_jake_list,0)

jake_list = ['jake','jake & his subconscious','jake (in flashback)','jake (voiceover)',"jake [in bmo's dream]",'jake [in flashback]','jake [offscreen]','jake [on phone]','jake [on voicemail]','jake [the one watching the video]','jake [voice-over]',"jake's elbow","jake's subconscious",'past jake','pictured jake','puppy jake','dream jake','dream jake (slowly)','flashback jake', 'future jake','giant jake']
jake_df = combine_names_in_list(jake_list,0)

marceline_list = ['marceline','marc','marcelince','marceline and ghosts','marcy','teenage marceline','young marceline' ]
marceline_df = combine_names_in_list(marceline_list,0)

bubblegum_list = ['princess bubblegum','princes bubblegum', "princess bubblegum [finn's mind]", 'princess bubblegum [hologram]', "princess bubblegum [in finn's mind]", 'princess bubblegum [in real world]', 'princess bubblegum [in video]','princess bubblegum [voice-over]', "princess bubblegum's voice [in finn's head]", 'princess bubblegun', 'princess bubblgum', 'bubblegum', 'hallucination of princess bubblegum', 'pb']
bubblegum_df = combine_names_in_list(bubblegum_list,0)

all_dfs = [banana_df,susan_df,cake_df,tiffany_df,finn_and_jake_df,bubblegum_df,fern_df,gunter_df,flame_princess_df,
    king_ooo_df,lady_df,pbutler_df,simon_df,starchie_df,cinnabun_df,marshall_df,joshua_df,tree_trunks_df,bmo_df,
    magic_man_df,lemonhope_df,lemongrabs_df,lemongrab_df,other_lemongrab_df,lich_df,ice_king_df,normal_man_df,
    fionna_df,death_df,sweetp_df,football_df,lsp_df,betty_df,hunson_df,finn_df,jake_df,marceline_df,prince_gumball_df]

big_df = pd.concat(all_dfs)

big_df.to_pickle("./adventure_pickle_CLEAN.pkl")
