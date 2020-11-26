# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 10:55:25 2020

@author: JassonM0lina
"""

import numpy as np
import ga
import objective
import matplotlib.pyplot as plt
from itertools import combinations
from time import process_time
import random
import math



def mesh_general(agent_active,maximum,bounds,novelties_aux_cap,ga_param,enc_dec):
    
    lower_bounds = bounds[0]
    upper_bounds = bounds[1]
        
    
    pop_size = ga_param[0] 
    crossover_rate = ga_param[1]
    mutation_rate = ga_param[2] 
    no_generations = ga_param[3] 
    step_size = ga_param[4] 
    rate = ga_param[5] 
    # Each variable correspond to an agent
    no_variables = agent_active.shape[0]


    # Initial population of genetic algoritm
    pop = np.zeros((pop_size,no_variables))
    for s in range(pop_size):
        for h in range(no_variables):
            pop[s,h] = np.random.random_integers(lower_bounds[h],upper_bounds[h])
    
    extended_pop = np.zeros((pop_size+crossover_rate+mutation_rate+2*no_variables*rate,pop.shape[1]))    
    
    g = 0
    global_best = np.zeros((no_generations+1,no_variables))

    # Evolution and new generation into the population
    while g <= no_generations:

        # crossover, mutation, fitness and local search function
        offspring1 = ga.crossover(pop, crossover_rate)
        offspring2 = ga.mutation(pop, mutation_rate)
        [fitness,diff,ag,dim]  = objective.objtv_gen_functn(pop,novelties_aux_cap,maximum,agent_active,enc_dec)
        offspring3 = ga.local_search(pop, fitness, lower_bounds, upper_bounds, step_size, rate)
        step_size = step_size*0.98
        if step_size<1:
            step_size = 1
            
        # Put into the previous population the new generations    
        extended_pop[0:pop_size] = pop
        extended_pop[pop_size:pop_size+crossover_rate] = offspring1
        extended_pop[pop_size+crossover_rate:pop_size+crossover_rate+mutation_rate]=offspring2
        extended_pop[pop_size+crossover_rate+mutation_rate:pop_size+crossover_rate+mutation_rate+2*no_variables*rate]=offspring3
        [fitness,diff,ag,dim]  = objective.objtv_gen_functn(extended_pop,novelties_aux_cap,maximum,agent_active,enc_dec)
        pop = ga.selection(extended_pop, fitness, pop_size)
        
        print("Generation: ", g, ", current fitness value: ", min(fitness))
        
        # Find the local minimum (local solution)
        index = np.argmin(fitness)
        current_best = extended_pop[index]
        global_best[g]=current_best
        g +=1
    
    # Find the global minimum (global solution)
    [fitness,diff,ag,dim]  = objective.objtv_gen_functn(global_best,novelties_aux_cap,maximum,agent_active,enc_dec)
    index = np.argmin(fitness)
    print("Best solution = ", np.ceil(global_best[index]))
    print("Best fitness value= ", min(fitness))    
    best = np.ceil(global_best[index])
    #dife = diff[index]
    prog = ag[index]
    nes = np.ceil(maximum)
    
    dim = []
    count_static = 0
    for j in range(best.shape[0]):           
        if agent_active[j] == 'NO':                
           assign = novelties_aux_cap[0][int(best[j])]
           dim.append(assign)               
           
        elif agent_active[j] == 'AM':    
           assign = novelties_aux_cap[1][int(best[j])]
           dim.append(assign)  
           
        elif agent_active[j] == 'PM':     
           assign = novelties_aux_cap[2][int(best[j])]
           dim.append(assign)  
           
        elif agent_active[j] == 'MAMA':
           assign = novelties_aux_cap[3][int(best[j])]
           dim.append(assign) 
           
        elif agent_active[j] == 'SEDE':
           assign = novelties_aux_cap[4][int(best[j])]
           dim.append(assign)      
        
        elif agent_active[j] == 'ESPECIAL':            
               assign = novelties_aux_cap[5][int(best[j])]
               dim.append(assign)  
           
        else:
               assign = novelties_aux_cap[6][count_static][int(best[j])]
               dim.append(assign)
               count_static += 1
           
    # Plot the global solution
    plt.plot(prog,label="A. Programados")
    plt.plot(nes,label="A. Necesarios + 15%")
    plt.plot(nes/1.15,label="A. Necesarios")
    plt.plot(nes/(1.15*1.1333333),label="Llamadas")
    
    plt.grid()
    plt.legend()
    plt.axis('equal')
    plt.xlabel('Bloque de tiempo')
    plt.ylabel('No asesores')
    plt.title('programacion maxima entre semana')
    plt.show()
    
    return [best,prog,nes,dim]


def mesh_perday(agent_active,week,ga_param,enc_dec,days,dim):
        
    options_days = [i for i in combinations(range(len(days)-1),3)] 
    options_cap = np.random.randint(agent_active.shape[0], size=(5*agent_active.shape[0], int(agent_active.shape[0]/2)))
    
    lower_bounds = [0,0]
    upper_bounds = [len(options_days)-1,options_cap.shape[0]]
        
    t1_start = process_time()
    pop_size = ga_param[0] 
    crossover_rate = ga_param[1]
    mutation_rate = ga_param[2] 
    no_generations = ga_param[3] #300000000000
    step_size = (upper_bounds[1]-lower_bounds[1])*0.001#ga_param[4] 
    rate = ga_param[5] 
    computing_time = 30
    # Each variable correspond to an agent
    no_variables = 2


    # Initial population of genetic algoritm
    pop = np.zeros((pop_size,no_variables))
    for s in range(pop_size):
        for h in range(no_variables):
            pop[s,h] = np.random.uniform(lower_bounds[h],upper_bounds[h])
    
    extended_pop = np.zeros((pop_size+crossover_rate+mutation_rate+2*no_variables*rate,pop.shape[1]))    
    
    A = []
    a= 2  
    g = 0
    #global_best = np.zeros((no_generations+1,no_variables))
    global_best = pop[0]
    k=0
    # Evolution and new generation into the population
    while g <= no_generations:
        for i in range(no_generations):
            # crossover, mutation, fitness and local search function
            offspring1 = ga.crossover(pop, crossover_rate)
            offspring2 = ga.mutation(pop, mutation_rate)
            [fitness,ag1,ag2]  = objective.objtv_day_functn(pop,options_days,options_cap,week,agent_active,enc_dec,dim)
            offspring3 = ga.local_search(pop, fitness, lower_bounds, upper_bounds, step_size, rate)
            step_size = step_size*0.98
            if step_size<(upper_bounds[1]-lower_bounds[1])*0.001:
                step_size = (upper_bounds[1]-lower_bounds[1])*0.001
                
            # Put into the previous population the new generations    
            extended_pop[0:pop_size] = pop
            extended_pop[pop_size:pop_size+crossover_rate] = offspring1
            extended_pop[pop_size+crossover_rate:pop_size+crossover_rate+mutation_rate]=offspring2
            extended_pop[pop_size+crossover_rate+mutation_rate:pop_size+crossover_rate+mutation_rate+2*no_variables*rate]=offspring3
            [fitness,ag1,ag2]  = objective.objtv_day_functn(extended_pop,options_days,options_cap,week,agent_active,enc_dec,dim)
            pop = ga.selection(extended_pop, fitness, pop_size)
            
            print("Generation: ", g, ", current fitness value: ", min(fitness))
            
            # Find the local minimum (local solution)
            #index = np.argmin(fitness)
            #current_best = extended_pop[index]
            #global_best[g]=current_best
            A.append(min(fitness))
            g +=1
            if i>=a:
                if sum(abs(np.diff(A[g-a:g]))) <= 0.005:
                    index = np.argmin(fitness)
                    current_best = extended_pop[index]
                    pop = np.zeros((pop_size,no_variables))
                    for s in range(pop_size):#(pop_size - 1):
                        for h in range(no_variables):
                            pop[s,h] = np.random.uniform(lower_bounds[h], upper_bounds[h])
                    pop[pop_size - 1:pop_size] = current_best
                    step_size = (upper_bounds[1]-lower_bounds[1])*0.02
                    global_best = np.vstack((global_best,current_best))
                    #k +=1
                    break
        #     t1_stop = process_time()
        #     time_elapsed = t1_stop - t1_start
        #     if time_elapsed >= computing_time:
        #         break
        # if time_elapsed >= computing_time:
        #     break
                
    # Find the global minimum (global solution)
    [fitness,ag1,ag2]  = objective.objtv_day_functn(global_best,options_days,options_cap,week,agent_active,enc_dec,dim)
    index = np.argmin(fitness)
    print("Best solution = ", np.ceil(global_best[index]))
    print("Best fitness value= ", min(fitness))    
    best = np.ceil(global_best[index])
    #dife = diff[index]
    prog1 = ag1[index]
    prog2 = ag2[index]
    
    options_cap2 = {x for x in range(agent_active.shape[0])}
    options_cap2.difference_update(options_cap[int(best[1])])
    
    training = enc_dec[5]
    rostrng1 = np.asarray(dim)
    rostrng2 = np.asarray(dim)
    for j in options_cap[int(best[1])]: 
        for y in training:
            rostrng1[:][j][rostrng1[:][j] == y] = 1
    for k in options_cap2:
        for z in training:
            rostrng2[:][k][rostrng2[:][k] == z] = 1
        
    options_days2 = {x for x in range(len(week)-1)}
    options_days2.difference_update(options_days[int(best[0])])    
    
    rostrng1_dict = {}
    rostrng2_dict = {}
    for rostrn in range(len(dim)):
        rostrng1_dict[rostrn] = rostrng1[rostrn]
        rostrng2_dict[rostrn] = rostrng2[rostrn]
    
    rostrng_total = {}
    for i in options_days[int(best[0])]:
        rostrng_total[i] = rostrng1_dict
    for p in options_days2:
        rostrng_total[p] = rostrng2_dict
    
    return rostrng_total


def mesh_fds(agent_active,week,ga_param,enc_dec,rostrng_total,bounds_fds,novelties_aux_fds,new_nov_agent):
       
    
    fds_day = 1
    if all([np.isnan(x) for x in agent_active[:,3]]):
        fds_day = 0
    
        
    if fds_day == 1:
        training = enc_dec[5][0]
        agent_sun = list(np.where(agent_active[:,3] == 1)[0])
                    
        sat_train = set()
        for y in rostrng_total[5]:
            if training in rostrng_total[5][y]:
               sat_train.add(y)
            
        
        # try: 
        #     agent_sun = random.sample(sun,math.ceil(np.amax(week[6]))+8)
        # except:
        #     agent_sun = list(sun.copy())
            
            
        active_agent = {x for x in range(agent_active.shape[0])}
        
        agent_sat = list(np.where(agent_active[:,3] == 2)[0])
        
        sat_train.difference_update(agent_sun)
        
        agent_fds = [agent_sat,agent_sun]
        
        upp_bods = bounds_fds[1]
            
        low_bods_sat = np.zeros((1,len(agent_sat)))
        upp_bods_sat = np.zeros((1,len(agent_sat)))
        sat_nov = np.zeros((1,len(agent_sat)),dtype='O')
        count_sat = 0
        for p in agent_sat:  
            upp_bods_sat[0][count_sat] = upp_bods[p] 
            sat_nov[0][count_sat] = new_nov_agent[p]
            count_sat +=1
            
        low_bods_sun = np.zeros((1,len(agent_sun)))
        upp_bods_sun = np.zeros((1,len(agent_sun)))
        sun_nov = np.zeros((1,len(agent_sun)),dtype='O')
        count_sun = 0        
        for o in agent_sun:   
            upp_bods_sun[0][count_sun] = upp_bods[o] 
            sun_nov[0][count_sun] = new_nov_agent[o]
            count_sun +=1
        
        
        upper_bounds_total = [upp_bods_sat[0],upp_bods_sun[0]]
        lower_bounds_total = [low_bods_sat[0],low_bods_sun[0]]
        new_nov = [sat_nov[0],sun_nov[0]]
        
    if  fds_day == 0:  
        upper_bounds_total = [bounds_fds[1]]
        lower_bounds_total = [bounds_fds[0]]
        new_nov = [new_nov_agent]       
        agent_fds = [[x for x in range(agent_active.shape[0])]]
        
        
    pop_size = ga_param[0] 
    crossover_rate = ga_param[1]
    mutation_rate = ga_param[2] 
    no_generations = ga_param[3] 
    step_size = ga_param[4] 
    rate = ga_param[5] 
    # Each variable correspond to an agent
    
    for k in range(5,6+fds_day):        
        no_variables = len(agent_fds[k-5])
        
        upper_bounds = upper_bounds_total[k-5]
        lower_bounds =  lower_bounds_total[k-5]
        
        nov_agent = new_nov[k-5]        
        # Initial population of genetic algoritm
        pop = np.zeros((pop_size,no_variables))
        for s in range(pop_size):
            for h in range(no_variables):
                pop[s,h] = np.random.random_integers(lower_bounds[h],upper_bounds[h])
        
        extended_pop = np.zeros((pop_size+crossover_rate+mutation_rate+2*no_variables*rate,pop.shape[1]))    
        
        g = 0
        global_best = np.zeros((no_generations+1,no_variables))
    
        # Evolution and new generation into the population
        while g <= no_generations:
    
            # crossover, mutation, fitness and local search function
            offspring1 = ga.crossover(pop, crossover_rate)
            offspring2 = ga.mutation(pop, mutation_rate)
            [fitness,diff,ag,dim]  = objective.objtv_gen_functn(pop,novelties_aux_fds,week[k-5],nov_agent,enc_dec)
            offspring3 = ga.local_search(pop, fitness, lower_bounds, upper_bounds, step_size, rate)
            step_size = step_size*0.98
            if step_size<1:
                step_size = 1
                
            # Put into the previous population the new generations    
            extended_pop[0:pop_size] = pop
            extended_pop[pop_size:pop_size+crossover_rate] = offspring1
            extended_pop[pop_size+crossover_rate:pop_size+crossover_rate+mutation_rate]=offspring2
            extended_pop[pop_size+crossover_rate+mutation_rate:pop_size+crossover_rate+mutation_rate+2*no_variables*rate]=offspring3
            [fitness,diff,ag,dim]  = objective.objtv_gen_functn(extended_pop,novelties_aux_fds,week[k-5],nov_agent,enc_dec)
            pop = ga.selection(extended_pop, fitness, pop_size)
            
            print("Generation: ", g, ", current fitness value: ", min(fitness))
            
            # Find the local minimum (local solution)
            index = np.argmin(fitness)
            current_best = extended_pop[index]
            global_best[g]=current_best
            g +=1
    
        
        # Find the global minimum (global solution)
        [fitness,diff,ag,dim]  = objective.objtv_gen_functn(global_best,novelties_aux_fds,week[k-5],nov_agent,enc_dec)
        index = np.argmin(fitness)
        print("Best solution = ", np.ceil(global_best[index]))
        print("Best fitness value= ", min(fitness))    
        best = np.ceil(global_best[index])
        #dife = diff[index]
        prog = ag[index]
        nes = np.ceil(week[k])
    
        # Plot the global solution
        plt.plot(prog,label="A. Programados")
        plt.plot(nes,label="A. Necesarios + 15%")
        plt.plot(nes/1.15,label="A. Necesarios")
        plt.plot(nes/(1.15*1.1333333),label="Llamadas")
        
        plt.grid()
        plt.legend()
        plt.axis('equal')
        plt.xlabel('Bloque de tiempo')
        plt.ylabel('No asesores')
        plt.title('´programacion fds {}'.format(k-5))
        plt.show()
        
        dim = []
        count_static = 0
        for j in range(best.shape[0]):           
            if nov_agent[j] == 'NO':                
               assign = novelties_aux_fds[0][int(best[j])]
               dim.append(assign)               
               
            elif nov_agent[j] == 'AM':    
               assign = novelties_aux_fds[1][int(best[j])]
               dim.append(assign)  
               
            elif nov_agent[j] == 'PM':     
               assign = novelties_aux_fds[2][int(best[j])]
               dim.append(assign)  
               
            elif nov_agent[j] == 'MAMA':
               assign = novelties_aux_fds[3][int(best[j])]
               dim.append(assign) 
               
            elif nov_agent[j] == 'SEDE':
               assign = novelties_aux_fds[4][int(best[j])]
               dim.append(assign)                  
                              
            elif nov_agent[j] == 'ESPECIAL':            
                assign = novelties_aux_fds[5][int(best[j])]
                dim.append(assign)  
                
            else:
                assign = novelties_aux_fds[6][count_static][int(best[j])]
                dim.append(assign)
                count_static += 1
               
        rostrng = np.asarray(dim)
        rostrng_dict = {}    
        
        if fds_day == 1:
            if k == 5:       
                training = enc_dec[5]       
                sat_no_train = active_agent.difference(sat_train)
                count_train = 0
                for h in agent_sat:
                    if h in sat_no_train:
                        for y in training:
                            rostrng[:][count_train][rostrng[:][count_train] == y] = 1
                    count_train += 1
                
                for rostrn in range(len(dim)):
                    rostrng_dict[agent_sat[rostrn]] = rostrng[rostrn]               
            elif k == 6:
                training = enc_dec[5]
                for h in range(len(agent_sun)):
                    for y in training:
                        rostrng[:][h][rostrng[:][h] == y] = 1
                        
                for rostrn in range(len(dim)):
                    rostrng_dict[agent_sun[rostrn]] = rostrng[rostrn]
                    
        if fds_day == 0:
           for rostrn in range(len(dim)):
               rostrng_dict[agent_fds[0][rostrn]] = rostrng[rostrn]             
                    
        rostrng_total[k] = rostrng_dict
    return rostrng_total
    

# def aux_cap(lunch_key,best,agent_active,week,bounds_Rtg,aux_cap,ga_param,novelties):
    

#     # Initial population of genetic algoritm
#     pop = np.zeros((pop_size,no_variables))
#     for s in range(pop_size):
#         for h in range(no_variables):
#             pop[s,h] = np.random.random_integers(lower_bounds[h],upper_bounds[h])
    
#     extended_pop = np.zeros((pop_size+crossover_rate+mutation_rate+2*no_variables*rate,pop.shape[1]))    
    
#     g = 0
#     global_best = np.zeros((no_generations+1,no_variables))

#     # Evolution and new generation into the population
#     while g <= no_generations:

#         # crossover, mutation, fitness and local search function
#         offspring1 = ga.crossover(pop, crossover_rate)
#         offspring2 = ga.mutation(pop, mutation_rate)
#         [fitness,diff,ag,dim]  = objective.objfun_aux_cap(pop,aux_cap,week[0],agent_active,lunch_key,best,novelties)
#         offspring3 = ga.local_search(pop, fitness, lower_bounds, upper_bounds, step_size, rate)
#         step_size = step_size*0.98
#         if step_size<1:
#             step_size = 1
            
#         # Put into the previous population the new generations    
#         extended_pop[0:pop_size] = pop
#         extended_pop[pop_size:pop_size+crossover_rate] = offspring1
#         extended_pop[pop_size+crossover_rate:pop_size+crossover_rate+mutation_rate]=offspring2
#         extended_pop[pop_size+crossover_rate+mutation_rate:pop_size+crossover_rate+mutation_rate+2*no_variables*rate]=offspring3
#         [fitness,diff,ag,dim]  = objective.objfun_aux_cap(extended_pop,aux_cap,week[0],agent_active,lunch_key,best,novelties)
#         pop = ga.selection(extended_pop, fitness, pop_size)
        
#         print("Generation: ", g, ", current fitness value: ", min(fitness))
        
#         # Find the local minimum (local solution)
#         index = np.argmin(fitness)
#         current_best = extended_pop[index]
#         global_best[g]=current_best
#         g +=1

    
#     # Find the global minimum (global solution)
#     [fitness,diff,ag,dim]  = objective.objfun_aux_cap(global_best,aux_cap,week[0],agent_active,lunch_key,best,novelties)
#     index = np.argmin(fitness)
#     print("Best solution = ", global_best[index])
#     print("Best fitness value= ", min(fitness))    
#     best = np.ceil(global_best[index])
#     #dife = diff[index]
#     prog = ag[index]
#     nes = np.ceil(week[0])
    
#     return  [best,prog,nes,dim]





### -------------------------------------------------------------------------------
##  Database Connection
### -------------------------------------------------------------------------------     

# # Connect to the database "retencionfija_malla"
# db = mysql.connector.connect(
#   host="localhost",
#   user="root",
#   password="",
#   database="retencionfija_malla"
# )


# # Select into the database, all the information of agents active or work in home
# cursor = db.cursor()
# cursor.execute("SELECT name_ag FROM agent INNER JOIN state ON fk_idstate = idstate WHERE  state_info='CONEXIÓN REMOTA' OR state_info='ACTIVO'")
# state_db = cursor.fetchall()
# state_db = np.array(state_db)   

#no_variables = state_db.shape[0]  

### -------------------------------------------------------------------------------
##  steps of the GA
## --------------------------------------------------------------------------------
 # a = 5
 # if i >= a:
        #     if sum(abs(np.diff(A[g-a:g])))<=0.05:
        #         index = np.argmin(fitness)
        #         current_best = extended_pop[index]
        #         # pop = np.zeros((pop_size, no_variables))
        #         # for s in range(pop_size):
        #         #     for h in range(no_variables):
        #         #         pop[s,h]=np.random.uniform(lower_bounds[h],upper_bounds[h])
        #         step_size = 5
        #         global_best[k]=current_best
        #         k +=1
        #         break     
     
# minim = {}
# for t in range(dife.shape[0]-3):
#     if (dife[t] > 0 and dife[t+1] > 0 and dife[t+2] > 0 and dife[t+3] > 0):              
#         minim[t]= np.min([dife[t], dife[t+1], dife[t+2], dife[t+3]])
    

 # ### Plot about the evolution of the population
    # fig = plt.figure()
    # ax = fig.add_subplot()
    # fig.show()
    # plt.title('Evolutionary process of the objetive function value')
    # plt.xlabel('Iteration')
    # plt.ylabel('objetive function')
     

    # ax.plot(A,color='r')
    # fig.canvas.draw()
    # ax.set_xlim(left=max(0,g-no_generations),right = g+3)

    # plt.show()