# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 14:34:47 2020

@author: asus
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import mysql.connector
import tensorflow as tf
import strategy
import math
# Agents that are active 
ac = pd.read_excel('./Scheduling/agents_active/agents.xlsx', sheet_name='active',header=None)
agent_active = ac.to_numpy()


# Posible solutions (Scheduling for the agents) 
nonov = pd.read_excel('./Scheduling/solution_psb/solutions6a2200.xlsx', sheet_name='nonov',header=None).to_numpy()
eman =  pd.read_excel('./Scheduling/solution_psb/solutions6a2200.xlsx', sheet_name='eman',header=None).to_numpy()
etarde = pd.read_excel('./Scheduling/solution_psb/solutions6a2200.xlsx', sheet_name='etarde',header=None).to_numpy()
mama = pd.read_excel('./Scheduling/solution_psb/solutions6a2200.xlsx', sheet_name='mama',header=None).to_numpy()
novpar = pd.read_excel('./Scheduling/solution_psb/solutions6a2200.xlsx', sheet_name='novpar',header=None).to_numpy()
sede = pd.read_excel('./Scheduling/solution_psb/solutions6a2200.xlsx', sheet_name='sede',header=None).to_numpy()

# forecast for each block time
fct = pd.read_excel('./Forecasting/forecst.xlsx', sheet_name='forecst',header=None)
forcst = np.flip(fct.to_numpy())


# Parameters of the genetic algoritm (AI)    
lower_bounds = [0] * agent_active.shape[0]
pop_size = 100
crossover_rate = 50
mutation_rate = 50
no_generations = 98
step_size = 5
rate = 10

# Forecasting per day
monday = np.flip(forcst[0:int(forcst.shape[0]/7)][:,0])
tuesday = np.flip(forcst[int(forcst.shape[0]/7):int(forcst.shape[0]/7*2)][:,0])
wednesday = np.flip(forcst[int(forcst.shape[0]/7*2):int(forcst.shape[0]/7*3)][:,0])
thursday = np.flip(forcst[int(forcst.shape[0]/7*3):int(forcst.shape[0]/7*4)][:,0])
friday = np.flip(forcst[int(forcst.shape[0]/7*4):int(forcst.shape[0]/7*5)][:,0])
saturday = np.flip(forcst[int(forcst.shape[0]/7*5):int(forcst.shape[0]/7*6)][:,0])
sunday = np.flip(forcst[int(forcst.shape[0]/7*6):int(forcst.shape[0]/7*7)][:,0])


## ---------------------------------------------------------------------------
## Monday to Friday
## ---------------------------------------------------------------------------

# Specific parameters for monday to friday 
upper_bounds = []
for x in range(agent_active.shape[0]):
    if agent_active[x,1] == 'NO':
        upper_bounds.append(nonov.shape[1]-1)
    elif agent_active[x,1] == 'PM':    
        upper_bounds.append(eman.shape[1]-1)
    elif agent_active[x,1] == 'AM':     
        upper_bounds.append(etarde.shape[1]-1)
    elif agent_active[x,1] == 'MAMA':
        upper_bounds.append(mama.shape[1]-1)
    elif agent_active[x,1] == 'SEDE':
        upper_bounds.append(sede.shape[1]-1)    
    else:
        print("el agente ", agent_active[x][0], " tiene una novedad particular, generar un horario manual" )
        upper_bounds.append(novpar.shape[1]-1)
        
solutions = [nonov, eman, etarde, mama, novpar, sede]        
maximum = []
for d in range(int(forcst.shape[0]/7)):
    maximum.append(np.ceil(max([monday[d], tuesday[d], wednesday[d], thursday[d], friday[d]])))
   

[best,prog,nes] = strategy.mesh(agent_active[:,1],maximum,lower_bounds,upper_bounds,solutions,pop_size, crossover_rate,mutation_rate,no_generations,step_size,rate)

# Posible solutions (Scheduling for the agents) 
nonov_hor = pd.read_excel('./Scheduling/solution_psb/solutions6a2200.xlsx', sheet_name='nonov_hor',header=None).to_numpy()
eman_hor =  pd.read_excel('./Scheduling/solution_psb/solutions6a2200.xlsx', sheet_name='eman_hor',header=None).to_numpy()
etarde_hor = pd.read_excel('./Scheduling/solution_psb/solutions6a2200.xlsx', sheet_name='etarde_hor',header=None).to_numpy()
mama_hor = pd.read_excel('./Scheduling/solution_psb/solutions6a2200.xlsx', sheet_name='mama_hor',header=None).to_numpy()
novpar_hor = pd.read_excel('./Scheduling/solution_psb/solutions6a2200.xlsx', sheet_name='novpar_hor',header=None).to_numpy()
sede_hor = pd.read_excel('./Scheduling/solution_psb/solutions6a2200.xlsx', sheet_name='sede_hor',header=None).to_numpy()



horario={"asignacion": ['preturno', 'ingreso','salida','out capa','in capa','sal break1','ent break2','sal break2','sal break2',
                        'ent lunch', 'sal lunch']}
for h in range(best.shape[0]):
    ind = int(best[h])
    if agent_active[h,1] == 'NO':
        horario[agent_active[h][0]]= nonov_hor[ind].tolist()              
    elif agent_active[h,1] == 'PM':    
        horario[agent_active[h][0]]= eman_hor[ind].tolist()          
    elif agent_active[h,1] == 'AM':     
        horario[agent_active[h][0]]= etarde_hor[ind].tolist()  
    elif agent_active[h,1] == 'MAMA':
        horario[agent_active[h][0]]= mama_hor[ind].tolist()   
    elif agent_active[h,1] == 'SEDE':
        horario[agent_active[h][0]]= sede_hor[ind].tolist()       
    else:
        horario[agent_active[h][0]]= novpar_hor[ind].tolist()   

export = pd.DataFrame(horario)

with pd.ExcelWriter('./Rostering/agosto/10_16_agos_eyn.xlsx',engine="openpyxl",mode='a') as writer:
      export.to_excel(writer, sheet_name='horario',index = False) 

# si mañana, el trabajo es en la noche

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

# Plot monday
plt.plot(prog,label="A. Programados")
plt.plot(monday,label="A. Necesarios + 15%")
plt.plot(monday/1.15,label="A. Necesarios")
plt.plot(monday/(1.15*1.1333333),label="Llamadas")

plt.grid()
plt.legend()
plt.axis('equal')
plt.xlabel('Bloque de tiempo (15 min)')
plt.ylabel('No asesores')
plt.title('programacion Ret. fija, lunes')
plt.show()

# Plot tuesday
plt.plot(prog,label="A. Programados")
plt.plot(tuesday,label="A. Necesarios + 15%")
plt.plot(tuesday/1.15,label="A. Necesarios")
plt.plot(tuesday/(1.15*1.1333333),label="Llamadas")

plt.grid()
plt.legend()
plt.axis('equal')
plt.xlabel('Bloque de tiempo (15 min)')
plt.ylabel('No asesores')
plt.title('programacion Ret. fija, martes')
plt.show()

# Plot wednesday
plt.plot(prog,label="A. Programados")
plt.plot(wednesday,label="A. Necesarios + 15%")
plt.plot(wednesday/1.15,label="A. Necesarios")
plt.plot(wednesday/(1.15*1.1333333),label="Llamadas")

plt.grid()
plt.legend()
plt.axis('equal')
plt.xlabel('Bloque de tiempo (15 min)')
plt.ylabel('No asesores')
plt.title('programacion Ret. fija, miercoles')
plt.show()

# Plot thursday
plt.plot(prog,label="A. Programados")
plt.plot(thursday,label="A. Necesarios + 15%")
plt.plot(thursday/1.15,label="A. Necesarios")
plt.plot(thursday/(1.15*1.1333333),label="Llamadas")

plt.grid()
plt.legend()
plt.axis('equal')
plt.xlabel('Bloque de tiempo (15 min)')
plt.ylabel('No asesores')
plt.title('programacion Ret. fija, jueves')
plt.show()

# Plot friday
plt.plot(prog,label="A. Programados")
plt.plot(friday,label="A. Necesarios + 15%")
plt.plot(friday/1.15,label="A. Necesarios")
plt.plot(friday/(1.15*1.1333333),label="Llamadas")

plt.grid()
plt.legend()
plt.axis('equal')
plt.xlabel('Bloque de tiempo (15 min)')
plt.ylabel('No asesores')
plt.title('programacion Ret. fija, viernes')
plt.show()


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



