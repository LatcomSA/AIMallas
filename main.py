# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 14:34:47 2020

@author: JassonM0lina
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import mysql.connector
import tensorflow as tf
import strategy
import scheduling
import objective
import math


# Agents that are active 
agent_active = pd.read_excel('./Scheduling/Agents&Nov/agents_nov.xlsx', sheet_name='active',header=None).to_numpy()


# scheduling parameters for active agents

interval = 15 # Change 

init_hour = [7,0]
stop_hour = [22,15]

stop_hour_am = [17,45]
stop_hour_mther = [17,45]
stop_hour_sede = [15,45]

init_hour_pm = [13,0]

lunch_time_init = [12,0]
lunch_time_stop = [15,45]


laboral_time = [7,45]
lunch_hour_total = [1,0]
train_hour_total = [1,0]


# encode and decode information 
enc_dec = scheduling.encode_decode(interval, lunch_hour_total, train_hour_total)

# forecast for each block time
fct = pd.read_excel('./Forecasting/forecst.xlsx', sheet_name='forecst',header=None)
forcst = np.flip(fct.to_numpy())

# Forecasting per day
monday = np.flip(forcst[0:int(forcst.shape[0]/7)][:,0])
tuesday = np.flip(forcst[int(forcst.shape[0]/7):int(forcst.shape[0]/7*2)][:,0])
wednesday = np.flip(forcst[int(forcst.shape[0]/7*2):int(forcst.shape[0]/7*3)][:,0])
thursday = np.flip(forcst[int(forcst.shape[0]/7*3):int(forcst.shape[0]/7*4)][:,0])
friday = np.flip(forcst[int(forcst.shape[0]/7*4):int(forcst.shape[0]/7*5)][:,0])
saturday = np.flip(forcst[int(forcst.shape[0]/7*5):int(forcst.shape[0]/7*6)][:,0])
sunday = np.flip(forcst[int(forcst.shape[0]/7*6):int(forcst.shape[0]/7*7)][:,0])


# Parameters of the genetic algoritm (AI)    
pop_size = 100
crossover_rate = 50
mutation_rate = 50
no_generations = 50
step_size = 5
rate = 10




## ---------------------------------------------------------------------------
## General Dimensionig 
## ---------------------------------------------------------------------------

hour_time =[init_hour, stop_hour, laboral_time, stop_hour_am, 
            init_hour_pm, stop_hour_mther, stop_hour_sede,
            lunch_time_init, lunch_time_stop,lunch_hour_total]                                                                                                          


novelties = scheduling.schedul_gen(interval, hour_time)


novelties_aux_cap = scheduling.sched_aux_cap(interval, novelties, hour_time)

bounds = scheduling.sched_bounds_ga(novelties_aux_cap, agent_active)

ga_param = [pop_size,crossover_rate,mutation_rate,no_generations,step_size,rate]  
             
maximum = []
for d in range(int(forcst.shape[0]/7)):
    maximum.append(np.ceil(max([monday[d], tuesday[d], wednesday[d], thursday[d], friday[d]])))
   

[best,prog,nes,dim] = strategy.mesh(agent_active[:,1],maximum,bounds,novelties_aux_cap,ga_param,enc_dec)


# Plot the global solution
plt.plot(prog,label="A. Programados")
plt.plot(nes,label="A. Necesarios + 15%")
plt.plot(nes/1.15,label="A. Necesarios")
plt.plot(nes/(1.15*1.1333333),label="Llamadas")

plt.grid()
plt.legend()
plt.axis('equal')
plt.xlabel('Bloque de tiempo (15 min)')
plt.ylabel('No asesores')
plt.title('programacion Ret. fija, maximo')
plt.show()


## ---------------------------------------------------------------------------
## Rostering
## ---------------------------------------------------------------------------


# without_l = aux_cap[0]
# with_l = aux_cap[1]

# lunch_init = lunch_key[0]
# lunch_stop = lunch_key[1]

# lower_bounds_Rtg = [0]*agent_active.shape[0]
# upper_bounds_Rtg = []    

# for x in range(agent_active.shape[0]):
#     if agent_active[x,1] == 'NO':
#        if  lunch_init < best[x] < lunch_stop:
#            upper_bounds_Rtg.append(with_l.shape[1]-1)
#        else:
#            upper_bounds_Rtg.append(without_l.shape[1]-1)
           
#     elif agent_active[x,1] == 'AM':    
#        if lunch_init < best[x] < lunch_stop:
#            upper_bounds_Rtg.append(with_l.shape[1]-1)
#        else:
#            upper_bounds_Rtg.append(without_l.shape[1]-1)       
        
#     elif agent_active[x,1] == 'PM':             
#         upper_bounds_Rtg.append(without_l.shape[1]-1)
        
#     elif agent_active[x,1] == 'MAMA':
#        if  lunch_init < best[x] < lunch_stop:
#            upper_bounds_Rtg.append(with_l.shape[1]-1)
#        else:
#            upper_bounds_Rtg.append(without_l.shape[1]-1)        
        
#     elif agent_active[x,1] == 'SEDE':        
#         upper_bounds_Rtg.append(without_l.shape[1]-1)
        
#     else:
#         upper_bounds_Rtg.append(0) 

# bounds_Rtg = [lower_bounds_Rtg,upper_bounds_Rtg]

# ga_param = [pop_size,crossover_rate,mutation_rate,no_generations,step_size,rate]   

# week = np.ceil([monday,tuesday,wednesday,thursday,friday])

# [bes,pro,ne,di] = strategy.aux_cap(lunch_key,best,agent_active[:,1],week,bounds_Rtg,aux_cap,ga_param,novelties)

# # Plot the global solution
# plt.plot(pro,label="A. Programados")
# plt.plot(ne,label="A. Necesarios + 15%")
# plt.plot(ne/1.15,label="A. Necesarios")
# plt.plot(ne/(1.15*1.1333333),label="Llamadas")

# plt.grid()
# plt.legend()
# plt.axis('equal')
# plt.xlabel('Bloque de tiempo (15 min)')
# plt.ylabel('No asesores')
# plt.title('programacion Ret. fija, lunes')
# plt.show()
# novelties[0][best[0]][int(best[0]):int(best[0])+32]



## ---------------------------------------------------------------------------
## Sunday 
## ---------------------------------------------------------------------------

# agent_sun = []
# agent_saturday = []
# for i in range(agent_active.shape[0]):
#     if agent_active[i,2]<3:
#        agent_sun.append(agent_active[i,:]) 
#     elif agent_active[i,2]==3:
#        agent_saturday.append(agent_active[i,0]) 
       
# agent_sunday = np.array(agent_sun[0:math.ceil(max(sunday))+1])
# # Parameters of the genetic algoritm (AI)    
# upper_bounds_sun = []
# for x in range(len(agent_sunday)):
#     if agent_sunday[x,1] == 'nn':
#         upper_bounds_sun.append(nonov.shape[1]-1)
#     elif agent_sunday[x,1] == 'em':    
#         upper_bounds_sun.append(nonov.shape[1]-1)
#     elif agent_sunday[x,1] == 'en':     
#         upper_bounds_sun.append(nonov.shape[1]-1)
#     elif agent_sunday[x,1] == 'm':
#         upper_bounds_sun.append(mama.shape[1]-1)
#     else :
#         upper_bounds_sun.append(novpar.shape[1]-1)       

# solutions_sun = [nonov, nonov, nonov, mama, novpar]

# [sun_best,sun_prog,sun_nes] = strategy.mesh(agent_sunday[:,0],sunday,lower_bounds,upper_bounds_sun,solutions_sun,pop_size, crossover_rate,mutation_rate,no_generations,step_size,rate)

# ## ---------------------------------------------------------------------------
# ## Saturday
# ## ---------------------------------------------------------------------------

# agent_sat2 = agent_sun[math.ceil(max(sunday))+1:len(agent_sun)]

# for x in range(len(agent_sat2)):
#     agent_saturday.append(agent_sat2[x])


# [sat_best,sat_prog,sat_nes] = strategy.mesh(agent_saturday,saturday,lower_bounds,upper_bounds,solutions,pop_size, crossover_rate,mutation_rate,no_generations,step_size,rate)


##### Posible solutions (Scheduling for the agents) 
# nonov_hor = pd.read_excel('./Scheduling/solution_psb/solutions6a2200.xlsx', sheet_name='nonov_hor',header=None).to_numpy()
# eman_hor =  pd.read_excel('./Scheduling/solution_psb/solutions6a2200.xlsx', sheet_name='eman_hor',header=None).to_numpy()
# etarde_hor = pd.read_excel('./Scheduling/solution_psb/solutions6a2200.xlsx', sheet_name='etarde_hor',header=None).to_numpy()
# mama_hor = pd.read_excel('./Scheduling/solution_psb/solutions6a2200.xlsx', sheet_name='mama_hor',header=None).to_numpy()
# novpar_hor = pd.read_excel('./Scheduling/solution_psb/solutions6a2200.xlsx', sheet_name='novpar_hor',header=None).to_numpy()
# sede_hor = pd.read_excel('./Scheduling/solution_psb/solutions6a2200.xlsx', sheet_name='sede_hor',header=None).to_numpy()

# horario={"asignacion": ['preturno', 'ingreso','salida','out capa','in capa','sal break1','ent break2','sal break2','sal break2',
#                         'ent lunch', 'sal lunch']}
# for h in range(best.shape[0]):
#     ind = int(best[h])
#     if agent_active[h,1] == 'NO':
#         horario[agent_active[h][0]]= nonov_hor[ind].tolist()              
#     elif agent_active[h,1] == 'PM':    
#         horario[agent_active[h][0]]= eman_hor[ind].tolist()          
#     elif agent_active[h,1] == 'AM':     
#         horario[agent_active[h][0]]= etarde_hor[ind].tolist()  
#     elif agent_active[h,1] == 'MAMA':
#         horario[agent_active[h][0]]= mama_hor[ind].tolist()   
#     elif agent_active[h,1] == 'SEDE':
#         horario[agent_active[h][0]]= sede_hor[ind].tolist()       
#     else:
#         horario[agent_active[h][0]]= novpar_hor[ind].tolist()   

# export = pd.DataFrame(horario)

# with pd.ExcelWriter('./Rostering/agosto/10_16_agos_eyn.xlsx',engine="openpyxl",mode='a') as writer:
#       export.to_excel(writer, sheet_name='horario',index = False) 

## plots

# # Plot monday
# plt.plot(prog,label="A. Programados")
# plt.plot(monday,label="A. Necesarios + 15%")
# plt.plot(monday/1.15,label="A. Necesarios")
# plt.plot(monday/(1.15*1.1333333),label="Llamadas")

# plt.grid()
# plt.legend()
# plt.axis('equal')
# plt.xlabel('Bloque de tiempo (15 min)')
# plt.ylabel('No asesores')
# plt.title('programacion Ret. fija, lunes')
# plt.show()

# # Plot tuesday
# plt.plot(prog,label="A. Programados")
# plt.plot(tuesday,label="A. Necesarios + 15%")
# plt.plot(tuesday/1.15,label="A. Necesarios")
# plt.plot(tuesday/(1.15*1.1333333),label="Llamadas")

# plt.grid()
# plt.legend()
# plt.axis('equal')
# plt.xlabel('Bloque de tiempo (15 min)')
# plt.ylabel('No asesores')
# plt.title('programacion Ret. fija, martes')
# plt.show()

# # Plot wednesday
# plt.plot(prog,label="A. Programados")
# plt.plot(wednesday,label="A. Necesarios + 15%")
# plt.plot(wednesday/1.15,label="A. Necesarios")
# plt.plot(wednesday/(1.15*1.1333333),label="Llamadas")

# plt.grid()
# plt.legend()
# plt.axis('equal')
# plt.xlabel('Bloque de tiempo (15 min)')
# plt.ylabel('No asesores')
# plt.title('programacion Ret. fija, miercoles')
# plt.show()

# # Plot thursday
# plt.plot(prog,label="A. Programados")
# plt.plot(thursday,label="A. Necesarios + 15%")
# plt.plot(thursday/1.15,label="A. Necesarios")
# plt.plot(thursday/(1.15*1.1333333),label="Llamadas")

# plt.grid()
# plt.legend()
# plt.axis('equal')
# plt.xlabel('Bloque de tiempo (15 min)')
# plt.ylabel('No asesores')
# plt.title('programacion Ret. fija, jueves')
# plt.show()

# # Plot friday
# plt.plot(prog,label="A. Programados")
# plt.plot(friday,label="A. Necesarios + 15%")
# plt.plot(friday/1.15,label="A. Necesarios")
# plt.plot(friday/(1.15*1.1333333),label="Llamadas")

# plt.grid()
# plt.legend()
# plt.axis('equal')
# plt.xlabel('Bloque de tiempo (15 min)')
# plt.ylabel('No asesores')
# plt.title('programacion Ret. fija, viernes')
# plt.show()