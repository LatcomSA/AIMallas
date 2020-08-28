# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 15:48:24 2020

@author: JassonM0lina
"""


import numpy as np
import math
import statistics


def objtv_gen_functn(pop,novelties_aux_cap,maximum,agent_active,enc_dec):
    
    entry = enc_dec[1]
    departure = enc_dec[2]
    break1 = enc_dec[3]
    break2 = enc_dec[4]
    training = enc_dec[5]
    lunch = enc_dec[6]
    
    fitness = np.zeros(pop.shape[0])
    diff = []
    ag = []
    req = []
    #pop = np.round(pop)

    for i in range(pop.shape[0]):
        x = pop[i]
        dim = []
        for j in range(x.shape[0]):           
            if agent_active[j] == 'NO':                
               assign = novelties_aux_cap[0][int(x[j])]
               dim.append(assign)               
               
            elif agent_active[j] == 'AM':    
               assign = novelties_aux_cap[1][int(x[j])]
               dim.append(assign)  
               
            elif agent_active[j] == 'PM':     
               assign = novelties_aux_cap[2][int(x[j])]
               dim.append(assign)  
               
            elif agent_active[j] == 'MAMA':
               assign = novelties_aux_cap[3][int(x[j])]
               dim.append(assign) 
               
            elif agent_active[j] == 'SEDE':
               assign = novelties_aux_cap[4][int(x[j])]
               dim.append(assign)                  
               
            else:
               assign = novelties_aux_cap[5][int(x[j])]
               dim.append(assign)     
        
        dim_enc = np.array(dim)
    
        dim_enc[dim_enc == entry] = 1
        dim_enc[dim_enc == departure] = 1
        dim_enc[dim_enc == break1] = 0
        dim_enc[dim_enc == break2] = 0
        
        for x in training:
            dim_enc[dim_enc ==x] = 0
    
        for y in lunch:
            dim_enc[dim_enc == y] = 0
        
        agents = np.array(dim_enc).sum(axis=0)
        ag.append(agents)
        req.append(maximum)
        diff.append(agents - maximum)
        fitness[i]= (((agents-maximum)**2).sum(axis=0))**(1/2)
        #statistics.stdev(agents - maximum)    
        
    return [fitness,diff,ag,dim_enc] 

def objtv_day_functn(pop,options_days,options_cap,week,agent_active,enc_dec,dim):
    
    entry = enc_dec[1]
    departure = enc_dec[2]
    break1 = enc_dec[3]
    break2 = enc_dec[4]
    training = enc_dec[5]
    lunch = enc_dec[6]
    
    fitness = np.zeros(pop.shape[0])
    diff = []
    ag1 = []
    ag2 = []   

    for i in range(pop.shape[0]):
        x = pop[i]
        rostrng1 = np.asarray(dim)
        rostrng2 = np.asarray(dim)
        for h in options_cap[int(x[1])]: 
            for y in training:
                rostrng1[:][h][rostrng1[:][h] == y] = 1
                rostrng2[:][h][rostrng2[:][h] == y] = 0
        
        for p in training:
            rostrng1[rostrng1 == p] = 0
            rostrng2[rostrng2 == p] = 1        
               
        rostrng1[rostrng1 == entry] = 1
        rostrng1[rostrng1 == departure] = 1
        rostrng1[rostrng1 == break1] = 0
        rostrng1[rostrng1 == break2] = 0
        
        rostrng2[rostrng2 == entry] = 1
        rostrng2[rostrng2 == departure] = 1
        rostrng2[rostrng2 == break1] = 0
        rostrng2[rostrng2 == break2] = 0
        
    
        for l in lunch:
            rostrng1[rostrng1 == l] = 0  
            rostrng2[rostrng2 == l] = 0
    
        
        agents1 = np.array(rostrng1).sum(axis=0)
        agents2 = np.array(rostrng2).sum(axis=0)
        
        ag1.append(agents1)
        ag2.append(agents2)
        
        fitness[i] = 0
        for d in range(len(week)-1):
            if d in options_days[int(x[0])]:
                fitness[i] += (((agents1 - week[d])**2).sum(axis=0))**(1/2) 
                #statistics.stdev(agents1 - week[d])
            else:
                fitness[i] += (((agents2 - week[d])**2).sum(axis=0))**(1/2) 
                #statistics.stdev(agents2 - week[d])
            
        
        
    return [fitness,ag1,ag2]
# [fitness,diff,ag,dim_enc] 


# def encode(assign,enc_dec):
    
#     entry = enc_dec[1]
#     departure = enc_dec[2]
#     break1 = enc_dec[3]
#     break2 = enc_dec[4]
#     training = enc_dec[5]
#     lunch = enc_dec[6]
    
#     for p in range(assign.shape[0]):
#         if assign[p] == entry or assign[p] == departure:
#            assign[p] = 1
#         elif assign[p] == break1 or assign[p] == break2:
#            assign[p] = 0 
#         elif any(assign[p] == training) or any(assign[p] == lunch): 
#            assign[p] = 0
           
#     return assign
     

# def objfun_aux_cap(pop,aux_cap,week,agent_active,lunch_key,best,novelties):
    
#     lunch_init = lunch_key[0]
#     lunch_stop = lunch_key[1]
    
#     without_l = aux_cap[0]
#     with_l = aux_cap[1]
    
#     fitness = np.zeros(pop.shape[0])
#     diff = []
#     ag = []
#     req = []
#     #pop = np.round(pop)

#     for i in range(pop.shape[0]):
#         x = pop[i]
#         dim = []
#         count = 0
#         for j in range(x.shape[0]):            
#             if count%2 == 1:
#                 if agent_active[j] == 'NO':
#                     if  lunch_init < best[j] < lunch_stop:
#                         assign = novelties[0][best[j]]
#                         new_assign = with_l[:,int(x[j])]
#                         assign[int(best[j])-2:int(best[j])+32+2] = new_assign
#                         dim.append(assign)
#                     else:
#                         assign = novelties[0][best[j]]
#                         new_assign = without_l[:,int(x[j])]
#                         assign[int(best[j]):int(best[j])+32] = new_assign
#                         dim.append(assign)
                       
#                 elif agent_active[j] == 'AM':    
#                     if lunch_init < best[j] < lunch_stop:
#                         assign = novelties[1][best[j]]
#                         new_assign = with_l[:,int(x[j])]
#                         assign[int(best[j])-2:int(best[j])+32+2] = new_assign
#                         dim.append(assign)
#                     else:
#                         assign = novelties[1][best[j]]
#                         new_assign = without_l[:,int(x[j])]
#                         assign[int(best[j]):int(best[j])+32] = new_assign
#                         dim.append(assign)      
                    
#                 elif agent_active[j] == 'PM':             
#                         assign = novelties[2][best[j]]
#                         new_assign = without_l[:,int(x[j])]
#                         assign[int(best[j]):int(best[j])+32] = new_assign
#                         dim.append(assign)
                        
#                 elif agent_active[j] == 'MAMA':
#                     if  lunch_init < best[j] < lunch_stop:
#                         assign = novelties[3][best[j]]
#                         new_assign = with_l[:,int(x[j])]
#                         assign[int(best[j])-2:int(best[j])+32+2] = new_assign
#                         dim.append(assign)
#                     else:
#                         assign = novelties[3][best[j]]
#                         new_assign = without_l[:,int(x[j])]
#                         assign[int(best[j]):int(best[j])+32] = new_assign
#                         dim.append(assign)     
                    
#                 elif agent_active[j] == 'SEDE':        
#                         assign = novelties[4][best[j]]
#                         new_assign = without_l[:,int(x[j])]
#                         assign[int(best[j]):int(best[j])+32] = new_assign
#                         dim.append(assign)                
#                 else:
#                     assign = novelties[5][best[j]]
#                     dim.append(assign)
#             else:
#                 if agent_active[j] == 'NO':
#                         assign = novelties[0][best[j]]
#                         assign[int(best[j]):int(best[j])+32] = [1]*11+[0]+[1]*10+[0]+[1]*9
#                         dim.append(assign)
                       
#                 elif agent_active[j] == 'AM':    
#                         assign = novelties[1][best[j]]
#                         assign[int(best[j]):int(best[j])+32] = [1]*11+[0]+[1]*10+[0]+[1]*9
#                         dim.append(assign)      
                    
#                 elif agent_active[j] == 'PM':             
#                         assign = novelties[2][best[j]]
#                         assign[int(best[j]):int(best[j])+32] = [1]*11+[0]+[1]*10+[0]+[1]*9
#                         dim.append(assign)
                        
#                 elif agent_active[j] == 'MAMA':
#                         assign = novelties[3][best[j]]
#                         assign[int(best[j]):int(best[j])+32] = [1]*11+[0]+[1]*10+[0]+[1]*9
#                         dim.append(assign)     
                    
#                 elif agent_active[j] == 'SEDE':        
#                         assign = novelties[4][best[j]]
#                         assign[int(best[j]):int(best[j])+32] = [1]*11+[0]+[1]*10+[0]+[1]*9
#                         dim.append(assign)                
#                 else:
#                     assign = novelties[5][best[j]]
#                     dim.append(assign)
#             count +=1       
                
#         agents = np.array(dim).sum(axis=0)
#         ag.append(agents)
#         req.append(week)
#         diff.append(agents - week)
#         fitness[i]=statistics.stdev(agents - week)     
                
         
#     return [fitness,diff,ag,dim]       
            
        # agents = np.array(dim).sum(axis=0)
        # ag.append(agents)
        # req.append(maximum)
        # diff.append(agents - maximum)
        # fitness[i]=statistics.stdev(agents - maximum)
        
        
        # for x in range(agent_active.shape[0]):
        #     if agent_active[x,1] == 'NO':
        #        if  lunch_init < best[x] < lunch_stop:
        #            upper_bounds_Rtg.append(with_l.shape[1])
        #        else:
        #            upper_bounds_Rtg.append(without_l.shape[1])
                   
        #     elif agent_active[x,1] == 'AM':    
        #        if lunch_init < best[x] < lunch_stop:
        #            upper_bounds_Rtg.append(with_l.shape[1])
        #        else:
        #            upper_bounds_Rtg.append(without_l.shape[1])       
                
        #     elif agent_active[x,1] == 'PM':             
        #         upper_bounds_Rtg.append(without_l.shape[1])
                
        #     elif agent_active[x,1] == 'MAMA':
        #        if  lunch_init < best[x] < lunch_stop:
        #            upper_bounds_Rtg.append(with_l.shape[1])
        #        else:
        #            upper_bounds_Rtg.append(without_l.shape[1])        
                
        #     elif agent_active[x,1] == 'SEDE':        
        #         upper_bounds_Rtg.append(without_l.shape[1])
                
        #     else:
        #         upper_bounds_Rtg.append(0) 
        
        
    
     #[fitness,diff,ag,dim]

#
## -----------------------------------------------------------
    
  
# dim = []
# for j in range(best.shape[0]):           
#     if agent_active[j] == 'NO':
#         dim.append(solutions[0][int(best[j])])
#     elif agent_active[j] == 'AM':    
#         dim.append(solutions[1][int(best[j])]) 
#     elif agent_active[j] == 'PM':     
#         dim.append(solutions[2][int(best[j])]) 
#     elif agent_active[j] == 'MAMA':
#         dim.append(solutions[3][int(best[j])])
#     elif agent_active[j] == 'SEDE':
#         dim.append(solutions[4][int(best[j])])                  
#     else:
#         dim.append(solutions[5][int(best[j])])     

# dim.asarray(dim)

# hour_day = 24

# train_block = int(dim.shape[1]/hour_day)

# matrix_train = np.zeros((dim.shape)) 

# for i in range (dim.shape[0]):
#     for j in range(dim.shape[1]):
#         if (dim[i,j:j+4].sum() == 4):
#             matrix_train[i,j] = 1
            
    


# # ag.append(agents)
# # req.append(maximum)
# # diff.append(agents - maximum)
# # fitness[i]=statistics.stdev(agents - maximum)