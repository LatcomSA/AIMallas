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
    
    
    novelties = [no_nov, am_nov, pm_nov, mther_nov, sede_nov, spc_nov] 
    
    return novelties



def sched_aux_cap(interval, novelties, hour_time):

    
    min_hour = 60
    
    init_hour = hour_time[0]
    stop_hour = hour_time[1]
    
    laboral_time = hour_time[2] 
    
    lunch_time_init = hour_time[7] 
    lunch_time_stop = hour_time[8]
    lunch_hour_total = hour_time[9]
        
    
    lunch_min_total = int((lunch_hour_total[0]*min_hour + lunch_hour_total[0])/interval)
    total_block_laboral = int((laboral_time[0]*min_hour + laboral_time[1]+interval)/interval)
    total_block_laboral_lunch = total_block_laboral + lunch_min_total 
    
    
    lunch_init = ((lunch_time_init[0]*min_hour + lunch_time_init[1])/interval) - (total_block_laboral/2)
    lunch_stop = ((lunch_time_stop[0]*min_hour + lunch_time_stop[1] + interval)/interval) + (total_block_laboral/2) - total_block_laboral_lunch


    #stop_min = (stop_hour[0]*min_hour + stop_hour[1]) - (laboral_time[0]*min_hour + laboral_time[1]) - lunch_min_total
    
    #lunch_stop = min(lunch_stop,stop_min)

                    
    without_lunch = pd.read_excel('./Scheduling/Aux&Cap/aux_cap.xlsx', sheet_name=f"{interval}WL",header=None).to_numpy()
    with_lunch = pd.read_excel('./Scheduling/Aux&Cap/aux_cap.xlsx', sheet_name=f"{interval}L",header=None).to_numpy()
    

    
    no_nov = [] 
    for key,value in novelties[0].items():
        if  lunch_init <= key <= lunch_stop:
            for i in range(with_lunch.shape[1]): 
                assign = value.copy()
                new_assign = with_lunch[:,i]
                assign[key:key+total_block_laboral+lunch_min_total] = new_assign
                no_nov.append(assign)
        else:
            for i in range(without_lunch.shape[1]): 
                assign = value.copy()
                new_assign = without_lunch[:,i]
                assign[key:key+total_block_laboral] = new_assign
                no_nov.append(assign)
                
                
    am_nov = []
    for key,value in novelties[1].items():
        if  lunch_init <= key <= lunch_stop:
            for i in range(with_lunch.shape[1]): 
                assign = value.copy()
                new_assign = with_lunch[:,i]
                assign[key:key+total_block_laboral+lunch_min_total] = new_assign
                am_nov.append(assign)
        else:
            for i in range(without_lunch.shape[1]): 
                assign = value.copy()
                new_assign = without_lunch[:,i]
                assign[key:key+total_block_laboral] = new_assign
                am_nov.append(assign)  
                
    pm_nov = []
    for key,value in novelties[2].items():
        for i in range(without_lunch.shape[1]): 
            assign = value.copy()
            new_assign = without_lunch[:,i]
            assign[key:key+total_block_laboral] = new_assign
            pm_nov.append(assign)        
                
    
    mther_nov = [] 
    for key,value in novelties[3].items():
        if  lunch_init <= key <= lunch_stop:
            for i in range(with_lunch.shape[1]): 
                assign = value.copy()
                new_assign = with_lunch[:,i]
                assign[key:key+total_block_laboral+lunch_min_total] = new_assign
                mther_nov.append(assign)
        else:
            for i in range(without_lunch.shape[1]): 
                assign = value.copy()
                new_assign = without_lunch[:,i]
                assign[key:key+total_block_laboral] = new_assign
                mther_nov.append(assign)

    sede_nov = []
    for key,value in novelties[4].items():
        for i in range(without_lunch.shape[1]): 
            assign = value.copy()
            new_assign = without_lunch[:,i]
            assign[key:key+total_block_laboral] = new_assign
            sede_nov.append(assign)

    spc_nov = [novelties[5][0]]                
                
    
    novelties_aux_cap = [no_nov, am_nov, pm_nov, mther_nov, sede_nov, spc_nov] 

    return novelties_aux_cap

def sched_bounds_ga(novelties_aux_cap, agent_active):
    
    lower_bounds = [0]*agent_active.shape[0]
    upper_bounds = []    
    
    for x in range(agent_active.shape[0]):
        if agent_active[x,1] == 'NO':            
            upper_bounds.append(len(novelties_aux_cap[0])-1)
        elif agent_active[x,1] == 'AM':    
            upper_bounds.append(len(novelties_aux_cap[1])-1)
        elif agent_active[x,1] == 'PM':     
            upper_bounds.append(len(novelties_aux_cap[2])-1)
        elif agent_active[x,1] == 'MAMA':
            upper_bounds.append(len(novelties_aux_cap[3])-1)
        elif agent_active[x,1] == 'SEDE':
            upper_bounds.append(len(novelties_aux_cap[4])-1)
        else:
            upper_bounds.append(len(novelties_aux_cap[5])-1) 
    
    bounds = [lower_bounds, upper_bounds]
    
    return bounds


def encode_decode(interval, lunch_hour_total, train_hour_total):
    
    min_hour = 60     
    block_lunch_total = int((lunch_hour_total[0]*min_hour + lunch_hour_total[0])/interval)
    
    laboral = 1
    entry = 2
    departure = 3
    break1 = 4

    training = [i for i in range(break1+1,break1+block_lunch_total+1)]    
    lunch = [i for i in range(training[-1]+1,training[-1]+block_lunch_total+1)]
    
    break2 = lunch[-1]+1
    
    enc_dec = [laboral,entry,departure,break1,break2,training,lunch]
    
    return enc_dec
    
#def decode(dim):
        
    # aux_cap = [without_l,with_l]
    
    # #aux = [1]*11+[0]+[1]*11+[0]+[1]*9
    
    # if lunch_time_init[1] == 45:
    #    lunch_time_init[1] = 30 
    # elif lunch_time_init[1] == 15:
    #    lunch_time_init[1] = 0 
    
    # if lunch_time_stop[1] == 45:
    #    lunch_time_stop[1] = 30 
    # elif lunch_time_stop[1] == 15:
    #    lunch_time_stop[1] = 0 


# def aux(interval,laboral_time):
    
#     hour_day = 24
#     min_hour = 60
#     min_day = hour_day*min_hour
    
#     total_block_laboral = int((laboral_time[0]*min_hour + laboral_time[1]+interval)/interval)

#     # without lunch    
    
    
#     return
    
# lunch_key = [lunch_init,lunch_stop]

# #lower_bounds_Rtg = [0]*agent_active.shape[0]
# upper_bounds_Rtg = []   


# key_init = keys[0][0]
# key_stop = keys[0][1]

# key_init_am = keys[1][0]
# key_stop_am = keys[1][1]

# key_init_pm = keys[2][0]
# key_stop_pm = keys[2][1]

# key_init_mther = keys[3][0]
# key_stop_mther = keys[3][1]

# key_init_sede = keys[4][0]
# key_stop_sede = keys[4][1]


# aux_cap = [without_l,with_l]
    