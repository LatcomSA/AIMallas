# -*- coding: utf-8 -*-
"""
Created on Sun Aug  9 21:24:02 2020

@author: JassonM0lina
"""

import numpy as np
import pandas as pd


def schedul_gen(interval,hour_time):
    
    # parameters - organize the input information
    init_hour = hour_time[0]
    stop_hour = hour_time[1]
    
    laboral_time = hour_time[2]
    
    stop_hour_am = hour_time[3]
    init_hour_pm = hour_time[4]
    stop_hour_mther = hour_time[5]
    stop_hour_sede = hour_time[6]    
    
    hour_day = 24
    min_hour = 60
    min_day = hour_day*min_hour
    total_block_day = int(min_day/interval)
    
    total_block_laboral = int((laboral_time[0]*min_hour + laboral_time[1]+interval)/interval)
    no_block_laboral = total_block_day-total_block_laboral
    
    dic_time = {0: np.asarray([1]*total_block_laboral + [0]*no_block_laboral)}
    hour = range(interval,hour_day*min_hour,interval)
    dic_hour = {0: 0}
    
    ## total hash tables
    x = 1
    for t in hour:
        dic_time[x]= np.roll(dic_time[x-1],1)
        dic_hour[t]= x 
        x += 1
    
    ## without novelty
    
    init_min = init_hour[0]*min_hour + init_hour[1]
    stop_min = (stop_hour[0]*min_hour + stop_hour[1]) - (laboral_time[0]*min_hour + laboral_time[1])
        
    key_init = dic_hour.get(init_min)
    key_stop = dic_hour.get(stop_min) 
    
    no_nov = {}
    for n in range(key_init,key_stop+1):
        no_nov[n] = dic_time[n]
        
        
    ## novelty study afternoon so work am
    
    init_min_am = init_min
    stop_min_am = (stop_hour_am[0]*min_hour + stop_hour_am[1] - interval) - (laboral_time[0]*min_hour + laboral_time[1])
    
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
    stop_min_mther = (stop_hour_mther[0]*min_hour + stop_hour_mther[1] - interval) - (laboral_time[0]*min_hour + laboral_time[1])
    
    key_init_mther = dic_hour.get(init_min_mther)
    key_stop_mther = dic_hour.get(stop_min_mther) 
    
    mther_nov =  {}
    for a in range(key_init_mther,key_stop_mther+1):
        mther_nov[a] = dic_time[a]    
        
    ## novelty sede
        
    init_min_sede = init_min
    stop_min_sede = (stop_hour_sede[0]*min_hour + stop_hour_sede[1] - interval) - (laboral_time[0]*min_hour + laboral_time[1])
    
    key_init_sede = dic_hour.get(init_min_sede)
    key_stop_sede = dic_hour.get(stop_min_sede) 
    
    sede_nov =  {}
    for a in range(key_init_sede,key_stop_sede+1):
        sede_nov[a] = dic_time[a]    
    
    
    ## special novelty
        
    spc_nov = {0: np.asarray([0]*total_block_day)}
    
    
    # organize the outpt information
    keys = [[key_init, key_stop], [key_init_am,key_stop_am], 
            [key_init_pm, key_stop_pm], [key_init_mther,key_stop_mther],
            [key_init_sede,key_stop_sede]]
    
    novelties = [no_nov, am_nov, pm_nov, mther_nov, sede_nov, spc_nov] 
    
    return [keys, novelties]



def sched_aux_cap(interval, lunch_time):
    
    lunch_time_init = lunch_time[0]
    lunch_time_stop = lunch_time[1]
    
    min_hour = 60
    
    # scheduling for aux and cap
    without_l = pd.read_excel('./Scheduling/Aux&Cap/aux_cap.xlsx', sheet_name=f"{interval}WL",header=None).to_numpy()
    with_l = pd.read_excel('./Scheduling/Aux&Cap/aux_cap.xlsx', sheet_name=f"{interval}L",header=None).to_numpy()
    
    aux_cap = [without_l,with_l]
    
    #aux = [1]*11+[0]+[1]*11+[0]+[1]*9
    
    if lunch_time_init[1] == 45:
       lunch_time_init[1] = 30 
    elif lunch_time_init[1] == 15:
       lunch_time_init[1] = 0 
    
    if lunch_time_stop[1] == 45:
       lunch_time_stop[1] = 30 
    elif lunch_time_stop[1] == 15:
       lunch_time_stop[1] = 0 
    
    
    lunch_init = (lunch_time_init[0]*min_hour + lunch_time_init[0])/interval
    lunch_stop = (lunch_time_stop[0]*min_hour + lunch_time_stop[0])/interval
    
    lunch_key = [lunch_init,lunch_stop]
 
    return [lunch_key,aux_cap]


# def aux(interval,laboral_time):
    
#     hour_day = 24
#     min_hour = 60
#     min_day = hour_day*min_hour
    
#     total_block_laboral = int((laboral_time[0]*min_hour + laboral_time[1]+interval)/interval)

#     # without lunch    
    
    
#     return