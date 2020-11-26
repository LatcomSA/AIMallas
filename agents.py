0# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 13:20:09 2020

@author: JassonM0lina
"""

import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
#import mysql.connector

class Agent:
    def __init__(self,name,doc):
        self.name = name
        self.doc = doc
        self.graph = nx.Graph()

def agents_active(days):

    agent_active = pd.read_excel('./Scheduling/Agents&Nov/agents_nov.xlsx', sheet_name='active',header=None).to_numpy()
    
    sched_agent = {x: Agent(agent_active[x,0],agent_active[x,2]) for x in range(agent_active.shape[0])}
    
    for z in sched_agent:
        sched_agent.get(z).graph.add_node(sched_agent.get(z).name)
        for d in days:
              sched_agent.get(z).graph.add_edge(sched_agent.get(z).name,"{}_{}".format(d,sched_agent.get(z).name))
        #plt.show()
        #nx.draw(sched_agent.get(z).graph, with_labels=False)
    return [sched_agent,agent_active]        


# for w in range(1,num_weeks+1):
#   for d in days:  
#     for z in sched_agent:
#         sched_agent.get(z)
#         #addElement(sched_agent.get(z),w,sched_agent.get(z).element)
    
# for d in range(len(days)): 
#     for z in sched_agent:
#         for depth2 in sched_agent.get(z).info:
#             #addElement(depth2,days[d],depth2.element)

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

# class Agent:    
#     def __init__(self,element):
#         self.element = element
#         self.info = []