# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 10:55:25 2020

@author: Jasson M0lina
"""

import numpy as np
import ga
import objective
import matplotlib.pyplot as plt
import pandas as pd




def mesh(agent_active,maximum,lower_bounds,upper_bounds,solutions,pop_size,
               crossover_rate,mutation_rate,no_generations,step_size,rate):
    
    # Each variable correspond to an agent
    no_variables = agent_active.shape[0]

    # Initial population of genetic algoritm
    pop = np.zeros((pop_size,no_variables))
    for s in range(pop_size):
        for h in range(no_variables):
            pop[s,h] = np.random.uniform(lower_bounds[h],upper_bounds[h])
    
    extended_pop = np.zeros((pop_size+crossover_rate+mutation_rate+2*no_variables*rate,pop.shape[1]))
    
    # Plot about the evolution of the population
    fig = plt.figure()
    ax = fig.add_subplot()
    fig.show()
    plt.title('Evolutionary process of the objetive function value')
    plt.xlabel('Iteration')
    plt.ylabel('objetive function')
    
    
    A = []
    g = 0
    global_best = pop
    # Evolution and new generation into the population
    while g <= no_generations:
        for i in range(no_generations):
            # crossover, mutation, fitness and local search function
            offspring1 = ga.crossover(pop, crossover_rate)
            offspring2 = ga.mutation(pop, mutation_rate)
            [fitness,diff,ag]  = objective.objective_function(pop,solutions,maximum,agent_active)
            offspring3 = ga.local_search(pop, fitness, lower_bounds, upper_bounds, step_size, rate)
            step_size = step_size*0.98
            if step_size<1:
                step_size = 1
                
            # Put into the previous population the new generations    
            extended_pop[0:pop_size] = pop
            extended_pop[pop_size:pop_size+crossover_rate] = offspring1
            extended_pop[pop_size+crossover_rate:pop_size+crossover_rate+mutation_rate]=offspring2
            extended_pop[pop_size+crossover_rate+mutation_rate:pop_size+crossover_rate+mutation_rate+2*no_variables*rate]=offspring3
            [fitness,diff,ag]  = objective.objective_function(extended_pop,solutions,maximum,agent_active)
            pop = ga.selection(extended_pop, fitness, pop_size)
            
            A.append(max(fitness))
            print("Generation: ", g, ", current fitness value: ", A[g])
            
            # Find the local minimum (local solution)
            index = np.argmin(fitness)
            current_best = extended_pop[index]
            global_best[g]=current_best
            g +=1
            ax.plot(A,color='r')
            fig.canvas.draw()
            ax.set_xlim(left=max(0,g-no_generations),right = g+3)
            if g > no_generations:
                break
            if g > no_generations:
                break
    
    # Find the global minimum (global solution)
    [fitness,diff,ag]  = objective.objective_function(pop,solutions,maximum,agent_active)
    index = np.argmin(fitness)
    print("Best solution = ", global_best[index])
    print("Best fitness value= ", min(fitness))
    plt.show()
    
    best = np.round(global_best[index])
    #dife = diff[index]
    prog = ag[index]
    nes = np.ceil(maximum)

    return [best,prog,nes]








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
     