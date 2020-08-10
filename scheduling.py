# -*- coding: utf-8 -*-
"""
Created on Sun Aug  9 21:24:02 2020

@author: asus
"""

import numpy as np

interval = 15
init_hour = [7,0]
stop_hour = [22,15]

laboral_time = [7,45]

stop_hour_am = [17,45]
init_hour_pm = [13,0]
stop_hour_mther = [18,00]
stop_hour_sede = [16,0]


hour_day = 24
min_hour = 60
min_day = hour_day*min_hour
total_block_day = int(min_day/interval)

total_block_laboral = int((laboral_time[0]*min_hour + laboral_time[1]+15)/interval)
no_block_laboral = total_block_day-total_block_laboral

dic_time = {0: np.asarray([1]*total_block_laboral + [0]*no_block_laboral)}
hour = range(interval,hour_day*min_hour,interval)
dic_hour = {0: 0}

x = 1
for t in hour:
    dic_time[x]= np.roll(dic_time[x-1],1)
    dic_hour[t]= x 
    x += 1
    
init_min = init_hour[0]*min_hour + init_hour[1]
stop_min = (stop_hour[0]*min_hour + stop_hour[1]) - (laboral_time[0]*min_hour + laboral_time[1])
    
key_init = dic_hour.get(init_min)
key_stop = dic_hour.get(stop_min) 

## without novelty

no_nov = {}
for n in range(key_init,key_stop+1):
    no_nov[n] = dic_time[n]
    
    
## novelty study afternoon so work am

init_min_am = init_min
stop_min_am = (stop_hour_am[0]*min_hour + stop_hour_am[1] - 15) - (laboral_time[0]*min_hour + laboral_time[1])

key_init_am = dic_hour.get(init_min_am)
key_stop_am = dic_hour.get(stop_min_am) 

am_nov =  {}
for a in range(key_init_am,key_stop_am+1):
    am_nov[a] = dic_time[a]
    
## novelty study morning so work pm
    
stop_min_pm = stop_min
init_min_am = (init_hour_pm[0]*min_hour + init_hour_pm[1]) 

key_init_pm = dic_hour.get(init_min_am)
key_stop_pm = dic_hour.get(stop_min_pm)  

pm_nov =  {}
for p in range(key_init_pm,key_stop_pm+1):
    pm_nov[p] = dic_time[p] 
    

## novelty mother

init_min_mther = init_min
stop_min_mther = (stop_hour_mther[0]*min_hour + stop_hour_mther[1] - 15) - (laboral_time[0]*min_hour + laboral_time[1])

key_init_mther = dic_hour.get(init_min_mther)
key_stop_mther = dic_hour.get(stop_min_mther) 

mther_nov =  {}
for a in range(key_init_mther,key_stop_mther+1):
    mther_nov[a] = dic_time[a]    
    
## novelty sede
    
init_min_sede = init_min
stop_min_sede = (stop_hour_sede[0]*min_hour + stop_hour_sede[1] - 15) - (laboral_time[0]*min_hour + laboral_time[1])

key_init_sede = dic_hour.get(init_min_sede)
key_stop_sede = dic_hour.get(stop_min_sede) 

sede_nov =  {}
for a in range(key_init_sede,key_stop_sede+1):
    sede_nov[a] = dic_time[a]    


## special novelty
    
spc_nov = {0: np.asarray([1]*total_block_laboral + [0]*no_block_laboral)}

