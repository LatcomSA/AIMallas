# -*- coding: utf-8 -*-
"""
Created on Sun Aug  9 21:24:02 2020

@author: JassonM0lina
"""

import numpy as np
import pandas as pd
from math import nan
import datetime
from collections import OrderedDict 


def schedul_gen(interval,hour_time,agent_active_total):
    
    # parameters - organize the input information
    init_hour = hour_time[0]
    stop_hour = hour_time[1]
    
    laboral_time = hour_time[2]
    
    init_hour_am = hour_time[11]
    stop_hour_am = hour_time[3]
    init_hour_pm = hour_time[4]
    stop_hour_mther = hour_time[5]
    stop_hour_sede = hour_time[6]    
    
    init_hour_mther = hour_time[10]
    
    
    hour_day = 24
    min_hour = 60
    min_day = hour_day*min_hour
    total_block_day = int(min_day/interval)
    
    total_block_laboral = int((laboral_time[0]*min_hour + laboral_time[1])/interval)
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
    
    init_min_am = (init_hour_am[0]*min_hour + init_hour_am[1]) 
    stop_min_am = (stop_hour_am[0]*min_hour + stop_hour_am[1]) - (laboral_time[0]*min_hour + laboral_time[1])
    
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
    
    init_min_mther = (init_hour_mther[0]*min_hour + init_hour_mther[1]) 
    stop_min_mther = (stop_hour_mther[0]*min_hour + stop_hour_mther[1]) - (laboral_time[0]*min_hour + laboral_time[1])
    
    key_init_mther = dic_hour.get(init_min_mther)
    key_stop_mther = dic_hour.get(stop_min_mther) 
    
    mther_nov =  {}
    for a in range(key_init_mther,key_stop_mther+1):
        mther_nov[a] = dic_time[a]    
        
    ## novelty sede
        
    init_min_sede = init_min
    stop_min_sede = (stop_hour_sede[0]*min_hour + stop_hour_sede[1]) - (laboral_time[0]*min_hour + laboral_time[1])
    
    key_init_sede = dic_hour.get(init_min_sede)
    key_stop_sede = dic_hour.get(stop_min_sede) 
    
    sede_nov =  {}
    for a in range(key_init_sede,key_stop_sede+1):
        sede_nov[a] = dic_time[a]    
    
    
    ## special novelty
        
    spc_nov = {0: np.asarray([0]*total_block_day)}
    
    ## static novelty
    agent_active = agent_active_total[:,1]
    static_nov = {}
    count_static_nov = 0
    for agent in agent_active:
        try:
            order_stic_nov = OrderedDict() 
            hour_static = agent.split(" - ")
            init_static = datetime.datetime.strptime(hour_static[0],'%H:%M')
            stop_static = datetime.datetime.strptime(hour_static[1],'%H:%M')
            
            if stop_static.hour - init_static.hour  <= laboral_time[0]:
               order_stic_nov['lunch'] = 'no'
            else:
               order_stic_nov['lunch'] = 'yes'             
            init_min_static = init_static.hour*min_hour + init_static.minute
            key_init_static = dic_hour.get(init_min_static)
            order_stic_nov[key_init_static] = dic_time[key_init_static]                
            static_nov[count_static_nov] = order_stic_nov       
            count_static_nov += 1
        except:
            continue
        
    ## Static novelty fds
    agent_active_fds = agent_active_total[:,4]     
    new_nov_agent = np.zeros((1,agent_active.shape[0]),dtype='O')
    for y in range(agent_active.shape[0]):
        if agent_active_fds[y] is np.nan:
            if agent_active[y] == 'AM':
               new_nov_agent[0][y] = 'PM'
            elif agent_active[y] == 'PM':
               new_nov_agent[0][y] = 'AM'
            else:    
                new_nov_agent[0][y] =  agent_active[y]
        else:
            new_nov_agent[0][y] = agent_active_fds[y]
            
    static_nov_fd = {}
    count_static_nov_fds = 0
    for agent_fds in new_nov_agent[0]:
        try:
            order_stic_nov_fds = OrderedDict() 
            info_static_fds = agent_fds.split(" - ")
            init_static_fds = datetime.datetime.strptime(info_static_fds[0],'%H:%M')
            order_stic_nov_fds['fds_day'] = info_static_fds[1]    
            init_min_static_fds = init_static_fds.hour*min_hour + init_static_fds.minute
            key_init_static_fds = dic_hour.get(init_min_static_fds)
            order_stic_nov_fds[key_init_static_fds] = dic_time[key_init_static_fds]                
            static_nov_fd[count_static_nov_fds] = order_stic_nov_fds       
            count_static_nov_fds += 1
        except:
            continue
    
    novelties = [no_nov, am_nov, pm_nov, mther_nov, sede_nov, spc_nov, static_nov,static_nov_fd] 

        # try: 
    #     datetime.datetime.strptime(agent_active[y,1].split(" - ")[0],'%H:%M')
        
    # except:
    
    return novelties, new_nov_agent[0]



def sched_aux_cap(interval, novelties, hour_time,agent_active):

    
    min_hour = 60
    
    laboral_time = hour_time[2] 
    
    lunch_time_init = hour_time[7] 
    lunch_time_stop = hour_time[8]
    lunch_hour_total = hour_time[9]
        
    
    lunch_min_total = int((lunch_hour_total[0]*min_hour + lunch_hour_total[1])/interval)
    total_block_laboral = int((laboral_time[0]*min_hour + laboral_time[1])/interval)
    total_block_laboral_lunch = total_block_laboral + lunch_min_total 
    
    
    lunch_init = ((lunch_time_init[0]*min_hour + lunch_time_init[1])/interval) - (total_block_laboral/2)
    lunch_stop = ((lunch_time_stop[0]*min_hour + lunch_time_stop[1])/interval) + (total_block_laboral/2) - total_block_laboral_lunch

                    
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
            if lunch_init > key > lunch_stop:
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
            if lunch_init > key > lunch_stop:
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
            if lunch_init > key > lunch_stop:
                for i in range(without_lunch.shape[1]): 
                    assign = value.copy()
                    new_assign = without_lunch[:,i]
                    assign[key:key+total_block_laboral] = new_assign
                    mther_nov.append(assign)

    sede_nov = []
    for key,value in novelties[4].items():
        if  lunch_init <= key <= lunch_stop:
            for i in range(with_lunch.shape[1]): 
                assign = value.copy()
                new_assign = with_lunch[:,i]
                assign[key:key+total_block_laboral+lunch_min_total] = new_assign
                sede_nov.append(assign)
        for i in range(without_lunch.shape[1]): 
            assign = value.copy()
            new_assign = without_lunch[:,i]
            assign[key:key+total_block_laboral] = new_assign
            sede_nov.append(assign)

    spc_nov = [novelties[5][0]]   

    static_nov = {}
    for key_ttal,value_ttal in novelties[6].items():
        islunch = ''
        agent_static = []
        for key,value in value_ttal.items():
            if key == 'lunch':
               islunch = value
            else:
               if islunch == 'yes':
                for i in range(with_lunch.shape[1]): 
                    assign = value.copy()
                    new_assign = with_lunch[:,i]
                    assign[key:key+total_block_laboral+lunch_min_total] = new_assign
                    agent_static.append(assign)
               else: 
                for i in range(without_lunch.shape[1]): 
                    assign = value.copy()
                    new_assign = without_lunch[:,i]
                    assign[key:key+total_block_laboral] = new_assign
                    agent_static.append(assign)                    
        static_nov[key_ttal] = agent_static   
            
    
    novelties_aux_cap = [no_nov, am_nov, pm_nov, mther_nov, sede_nov, spc_nov,static_nov] 

    return novelties_aux_cap

def sched_aux_fds(interval, novelties, hour_time,agent_active):
    
    min_hour = 60   
    
    laboral_time = hour_time[2]          
    total_block_laboral = int((laboral_time[0]*min_hour + laboral_time[1])/interval)
                    
    without_lunch = pd.read_excel('./Scheduling/Aux&Cap/aux_cap.xlsx', sheet_name=f"{interval}WL",header=None).to_numpy()
    

    no_nov = [] 
    for key,value in novelties[0].items():
        for i in range(without_lunch.shape[1]): 
            assign = value.copy()
            new_assign = without_lunch[:,i]
            assign[key:key+total_block_laboral] = new_assign
            no_nov.append(assign)
                
                
    am_nov = []
    for key,value in novelties[1].items():
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

    static_nov_fds = {}
    for key_ttal,value_ttal in novelties[7].items():
        agent_static = []
        for key,value in value_ttal.items():
            if key != 'fds_day':
                for i in range(without_lunch.shape[1]): 
                    assign = value.copy()
                    new_assign = without_lunch[:,i]
                    assign[key:key+total_block_laboral] = new_assign
                    agent_static.append(assign)             
        static_nov_fds[key_ttal] = agent_static    
                
    
    novelties_aux_fds = [no_nov, am_nov, pm_nov, mther_nov, sede_nov, spc_nov,static_nov_fds]
    
    
    return novelties_aux_fds
    

def sched_bounds_ga(novelties_auxcap_gen, agent_active):
    
    lower_bounds = [0]*agent_active.shape[0]
    upper_bounds = []    
    
    static_count = 0
    for novelties in agent_active:
        if novelties == 'NO':            
            upper_bounds.append(len(novelties_auxcap_gen[0])-1)
        elif novelties == 'AM':    
            upper_bounds.append(len(novelties_auxcap_gen[1])-1)
        elif novelties == 'PM':     
            upper_bounds.append(len(novelties_auxcap_gen[2])-1)
        elif novelties == 'MAMA':
            upper_bounds.append(len(novelties_auxcap_gen[3])-1)
        elif novelties == 'SEDE':
            upper_bounds.append(len(novelties_auxcap_gen[4])-1)
        elif novelties == 'ESPECIAL':
            upper_bounds.append(len(novelties_auxcap_gen[5])-1) 
        else:
            upper_bounds.append(len(novelties_auxcap_gen[6][static_count])-1) 
            static_count += 1
                
    bounds = [lower_bounds, upper_bounds]
  
    return bounds


def encode_decode(interval, lunch_hour_total, train_hour_total):
    
    min_hour = 60     
    block_lunch_total = int((lunch_hour_total[0]*min_hour + lunch_hour_total[0])/interval)
    
    laboral = 1
    entry = 2
    departure = 3
    break1 = 4
    
    # training = [5,6]
    
    # lunch = [9,10]
    # break2 = [13]

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
    