# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 14:34:47 2020

@author: JassonM0lina
"""
import strategy
import scheduling
import agents
import rostering
import forecasting

# scheduling parameters for active agents

interval = 30 # Change 

init_hour = [7,0]
stop_hour = [23,0]

year = 2020
month = 9
day = 21
date = [day,month,year]

init_hour_am = [7,0]
stop_hour_am = [18,0]

stop_hour_sede = [19,0]

init_hour_mther = [7,0]
stop_hour_mther = [23,0]

init_hour_pm = [10,30]

lunch_time_init = [12,0]
lunch_time_stop = [15,30]

laboral_time = [8,0]

block_break = 1
lunch_hour_total = [1,0]
train_hour_total = [1,0]


hour_time =[init_hour, stop_hour, laboral_time, stop_hour_am, 
            init_hour_pm, stop_hour_mther, stop_hour_sede,
            lunch_time_init, lunch_time_stop,lunch_hour_total,init_hour_mther,
            init_hour_am]                                                   


days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']


# Parameters of the genetic algoritm (AI)    
pop_size = 100
crossover_rate = 50
mutation_rate = 50
no_generations = 40
step_size = 5
rate = 10

ga_param = [pop_size,crossover_rate,mutation_rate,no_generations,step_size,rate]  



## ---------------------------------------------------------------------------
## General Dimensionig 
## ---------------------------------------------------------------------------
[sched_agent,agent_active] = agents.agents_active(days)

[week,maximum] = forecasting.forecst() 

enc_dec = scheduling.encode_decode(interval, lunch_hour_total, train_hour_total)

novelties,new_nov_agent = scheduling.schedul_gen(interval, hour_time,agent_active)

novelties_aux_cap = scheduling.sched_aux_cap(interval, novelties, hour_time,agent_active[:,1])

bounds = scheduling.sched_bounds_ga(novelties_aux_cap, agent_active[:,1])

[best,prog,nes,dim] = strategy.mesh_general(agent_active[:,1],maximum,bounds,novelties_aux_cap,ga_param,enc_dec)

rostrng_total = strategy.mesh_perday(agent_active[:,1],week,ga_param,enc_dec,days,dim)

novelties_aux_fds= scheduling.sched_aux_fds(interval, novelties, hour_time, agent_active)

bounds_fds = scheduling.sched_bounds_ga(novelties_aux_fds, new_nov_agent)

rostrng_total = strategy.mesh_fds(agent_active,week,ga_param,enc_dec,rostrng_total,bounds_fds,novelties_aux_fds,new_nov_agent)

rostering.rostrng_info(rostrng_total,enc_dec,interval,lunch_hour_total, train_hour_total,block_break,sched_agent,agent_active)
    
sched_agent = rostering.rostrng_act(sched_agent,agent_active)

rostering.rostrng_doc(sched_agent,date)



#sht['A1'].value = pd.DataFrame(respta_info) 
            #columns= ['name','preturno', 'ingreso','salida','out capa','in capa','sal break1','ent break2','sal break2','sal break2','ent lunch', 'sal lunch'])          
                    
            

    
# horario={"asignacion": ['preturno', 'ingreso','salida','out capa','in capa','sal break1','ent break2','sal break2','sal break2',
#                         'ent lunch', 'sal lunch']}

# for x in sched_agent:
#     horario[sched_agent.get(x).name] = [sched_agent.get(x).preturn,
#                                         sched_agent.get(x).entry,
#                                         sched_agent.get(x).departure,
#                                         sched_agent.get(x).training_init,
#                                         sched_agent.get(x).training_stop,
#                                         sched_agent.get(x).break1_init,
#                                         sched_agent.get(x).break1_stop,
#                                         sched_agent.get(x).break2_init,
#                                         sched_agent.get(x).break2_stop,
#                                         sched_agent.get(x).lunch_init,
#                                         sched_agent.get(x).lunch_stop]

# export = pd.DataFrame(horario)

# with pd.ExcelWriter('./Rostering/agosto/24_28_agos_ret.xlsx',engine="openpyxl",mode='a') as writer:
#       export.to_excel(writer, sheet_name='horario',index = False) 



        # for z in sched_agent:
        #     sched_agent.get(z).graph.add_node(sched_agent.get(z).name)
        #     for w in range(1,num_weeks+1):
        #         week_agent = {sched_agent.get(z).name:w}
        #         sched_agent.get(z).graph.add_edge(sched_agent.get(z).name,w)
        #         for d in days:
        #             sched_agent.get(z).graph.add_edge(w,"{}_{}".format(d,w))
        # for t in total_auxs:
        #     sched_agent.get(z).graph.add_edge("{}_{}".format(x,w),"{}_{}_{}".format(t,d,w))
        #     for m in drtn:
        #         sched_agent.get(x).graph.add_edge("{}_{}_{}".format(t,d,w),"{}_{}_{}_{}".format(t,d,w,m))




# class Agent:    
#     def __init__(self,element):
#         self.element = element
#         self.info = []
#     def sched_preturn(agent,entry,interval,element,baseElement):
#         if entry == 0:           
#             h,m = divmod(((60*24)/interval-1)*interval,60)
#         else:   
#             h,m = divmod((entry-1)*interval,60)
#         self.preturn = datetime.time(h,m)
                   
#     def sched_entry(self,entry,interval):
#         h,m = divmod(entry*interval,60)
#         self.entry = datetime.time(h,m)
    
#     def sched_break1(self,break1,block_break,interval):
#         h,m = divmod(break1*interval,60)
#         h1,m1 = divmod((break1+block_break)*interval,60)
#         self.break1_init = datetime.time(h,m)
#         self.break1_stop = datetime.time(h1,m1)
        
#     def sched_break2(self, break2,block_break,interval):
#         h,m = divmod(break2*interval,60)
#         h1,m1 = divmod((break2+block_break)*interval,60)
#         self.break2_init = datetime.time(h,m)
#         self.break2_stop = datetime.time(h1,m1)
    
#     def sched_training(self,training,block_training,interval):    
#         h,m = divmod(training*interval,60)
#         h1,m1 = divmod((training+block_training)*interval,60)
#         self.training_init = datetime.time(h,m)
#         self.training_stop = datetime.time(h1,m1)
    
#     def sched_lunch(self,lunch,block_lunch,interval):
#         h,m = divmod(lunch*interval,60)
#         h1,m1 = divmod((lunch+block_lunch)*interval,60)
#         self.lunch_init = datetime.time(h,m)
#         self.lunch_stop = datetime.time(h1,m1)
    
#     def sched_departure(self,departure,interval):
#         h,m = divmod((departure+1)*interval,60)
#         self.departure = datetime.time(h,m)







# def addElement(agent,element,baseElement):
#     subelement = findAgent(agent,baseElement)   
#     subelement.info.append(Agent(element))
    
# def findAgent(agent,element):
#     if agent.element == element:
#         return agent
#     for agentGraph in agent.info:
#         Agentfinded = findAgent(agent,element)
#         if (Agentfinded != None):
#             return Agentfinded
#     return None
    

# sched_agent = {x: Agent(agent_active[x,0]) for x in range(agent_active.shape[0])}

# for w in range(1,num_weeks+1):
#     for z in sched_agent:
#         addElement(sched_agent.get(z),w,sched_agent.get(z).element)
    
# for d in range(len(days)): 
#     for z in sched_agent:
#         for depth2 in sched_agent.get(z).info:
#             addElement(depth2,days[d],depth2.element)



# def ejecutarProfundidadPrimero(arbol, funcion):
#     funcion(arbol.element)
#     for hijo in arbol.info:
#         ejecutarProfundidadPrimero(hijo, funcion)

# def printElement(element):
#     print(element)
# ejecutarProfundidadPrimero(sched_agent.get(4), printElement)

# def sched_preturn(agent,entry,interval,element,baseElement):
#     if entry == 0:           
#        h,m = divmod(((60*24)/interval-1)*interval,60)
#     else:   
#        h,m = divmod((entry-1)*interval,60)
#     subelement = buscarSubarbol(agent,baseElement)   
#     subelement.info.append(Agent(element))
#     self.preturn = datetime.time(h,m)

    # def sched_entry(self,entry,interval):
    #     h,m = divmod(entry*interval,60)
    #     self.entry = datetime.time(h,m)

#for z in 
            
# class agent:
    
#     def __init__(self,key,name):
#         self.key = key
#         self.name = name
  
        
#     nombre = ""
#     entry = ""
#     departure = ""
#     break1 = ""
#     break2 = ""
#     training = ""
#     lunch = ""


# for x in range(len(dim)):
#     for y in range(len(dim[x].shape[0])):
#         if dim[x][y] == entry:
            
    


# Plot monday
# plt.plot(prog1,label="A. Programados")
# plt.plot(week[0],label="A. Necesarios + 15%")
# plt.plot(week[0]/1.15,label="A. Necesarios")
# plt.plot(week[0]/(1.15*1.1333333),label="Llamadas")

# plt.grid()
# plt.legend()
# plt.axis('equal')
# plt.xlabel('Bloque de tiempo (15 min)')
# plt.ylabel('No asesores')
# plt.title('programacion Ret. fija, lunes')
# plt.show()

# # Plot tuesday
# plt.plot(prog1,label="A. Programados")
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
# plt.plot(prog1,label="A. Programados")
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
# plt.plot(prog2,label="A. Programados")
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
# plt.plot(prog2,label="A. Programados")
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


# days_active = [] 
# for x in range(len(days)):
#     if days[x] == 1:
#        days_active.append(x) 



# options_agent=[i for i in combinations(range(0,agent_active.shape[0]),int(agent_active.shape[0]/2))] 
# cbnt_agent = combinations(agent_num,int(agent_active.shape[0]/2))
# options_agent = []
# for i in list(cbnt_agent):
#     options_agent.append(i)
    


# perm = combinations(options, 2)   

# options2 = []
# for i in list(perm):
#     options2.append(i) 
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

