# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 15:48:24 2020

@author: asus
"""


import numpy as np
from math import ceil
import statistics


def objective_function(pop,solutions,maximum,agent_active):
  
    fitness = np.zeros(pop.shape[0])
    diff = []
    ag = []
    req = []
    pop = np.round(pop)

    for i in range(pop.shape[0]):
        x = pop[i]
        dim = []
        for j in range(x.shape[0]):           
            if agent_active[j] == 'NO':
               dim.append(solutions[0][:,int(x[j])])
            elif agent_active[j] == 'PM':    
               dim.append(solutions[1][:,int(x[j])]) 
            elif agent_active[j] == 'AM':     
               dim.append(solutions[2][:,int(x[j])]) 
            elif agent_active[j] == 'MAMA':
               dim.append(solutions[3][:,int(x[j])])
            elif agent_active[j] == 'SEDE':
               dim.append(solutions[5][:,int(x[j])])                  
            else:
               dim.append(solutions[4][:,int(x[j])])     
            
        agents = np.array(dim).sum(axis=0)
        ag.append(agents)
        req.append(maximum)
        diff.append(agents - maximum)
        fitness[i]=statistics.stdev(agents - maximum)
    return [fitness,diff,ag] 
