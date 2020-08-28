# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 10:55:25 2020

@author: JassonM0lina
"""

import numpy as np
import ga
import objective
import matplotlib.pyplot as plt
import pandas as pd
from itertools import combinations
from time import process_time


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
           
        else:
           assign = novelties_aux_cap[5][int(best[j])]
           dim.append(assign)   
           
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
    
    rostrng_total = {}
    for i in options_days[int(best[0])]:
        rostrng_total[i] = rostrng1
    for p in options_days2:
        rostrng_total[p] = rostrng2
    
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