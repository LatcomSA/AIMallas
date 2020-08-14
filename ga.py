# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 09:19:20 2020

@author: Jasson M0lina
"""

import numpy as np
import random
   

def selection(pop,fitness,pop_size):
    next_generation = np.zeros((pop_size,pop.shape[1]))
    elite = np.argmin(fitness)
    next_generation[0] = pop[elite]
    fitness = np.delete(fitness,elite)
    pop = np.delete(pop,elite,axis=0)
    P = [f/sum(fitness) for f in fitness]
    index = list(range(pop.shape[0]))
    index_selected = np.random.choice(index, size=pop_size-1, replace=False, p=P)
    s = 0
    for j in range(pop_size-1):
        next_generation[j+1] = pop[index_selected[s]]
        s +=1
    return next_generation


def crossover(pop,crossover_rate):
    offspring = np.zeros((crossover_rate,pop.shape[1]))
    for i in range(int(crossover_rate/2)):
        r1 = random.randint(0, pop.shape[0]-1)
        r2 = random.randint(0, pop.shape[0]-1)
        while r1 == r2:
            r1 = random.randint(0, pop.shape[0]-1)
            r2 = random.randint(0, pop.shape[0]-1)
        cutting_point = random.randint(1, pop.shape[1]-1)
        offspring[2*i, 0:cutting_point] = pop[r1, 0:cutting_point]
        offspring[2*i, cutting_point:] = pop[r2, cutting_point:]
        offspring[2*i+1, 0:cutting_point] = pop[r2, 0:cutting_point]
        offspring[2*i+1, cutting_point:] = pop[r1, cutting_point:]
    return offspring

def mutation(pop,mutation_rate):
    offspring = np.zeros((mutation_rate,pop.shape[1]))
    for i in range(int(mutation_rate/2)):
        r1 = random.randint(0, pop.shape[0]-1)
        r2 = random.randint(0, pop.shape[0]-1)
        while r1 == r2:
            r1 = random.randint(0, pop.shape[0]-1)
            r2 = random.randint(0, pop.shape[0]-1)
        cutting_point =random.randint(0, pop.shape[1]-1)
        offspring[2*i] = pop[r1]
        offspring[2*i,cutting_point] = pop[r2,cutting_point]
        offspring[2*i+1] = pop[r2]
        offspring[2*i+1,cutting_point] = pop[r1,cutting_point]
    return offspring

def local_search(pop,fitness,lower_bounds,upper_bounds,step_size,rate):
    index = np.argmin(fitness)
    offspring = np.zeros((rate*2*pop.shape[1],pop.shape[1]))
    for r in range(rate):
        offspring1 = np.zeros((pop.shape[1],pop.shape[1]))
        for i in range(int(pop.shape[1])):
            offspring1[i] = pop[index]
            offspring1[i,i] += np.random.uniform(0,step_size)
            if offspring1[i,i] > upper_bounds[i]:
                offspring1[i,i] = upper_bounds[i]
        offspring2 = np.zeros((pop.shape[1],pop.shape[1])) 
        for i in range(int(pop.shape[1])):
            offspring2[i] = pop[index]
            offspring2[i,i] += np.random.uniform(-step_size,0)
            if offspring2[i,i] < lower_bounds[i]:
                offspring2[i,i] = lower_bounds[i]
        offspring12 = np.zeros((2*pop.shape[1],pop.shape[1]))
        offspring12[0:pop.shape[1]] = offspring1
        offspring12[pop.shape[1]:2*pop.shape[1]] = offspring2
        offspring[r*2*pop.shape[1]:r*2*pop.shape[1]+2*pop.shape[1]]=offspring12
    return offspring


        
            
        