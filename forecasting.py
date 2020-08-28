# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 19:52:15 2020

@author: JassonM0lina
"""

import pandas as pd
import numpy as np

def forecst():
    fct = pd.read_excel('./Forecasting/forecst.xlsx', sheet_name='forecst',header=None)
    forcst = np.flip(fct.to_numpy())
    
    # Forecasting per day
    monday_fct = np.flip(forcst[0:int(forcst.shape[0]/7)][:,0])
    tuesday_fct = np.flip(forcst[int(forcst.shape[0]/7):int(forcst.shape[0]/7*2)][:,0])
    wednesday_fct = np.flip(forcst[int(forcst.shape[0]/7*2):int(forcst.shape[0]/7*3)][:,0])
    thursday_fct = np.flip(forcst[int(forcst.shape[0]/7*3):int(forcst.shape[0]/7*4)][:,0])
    friday_fct = np.flip(forcst[int(forcst.shape[0]/7*4):int(forcst.shape[0]/7*5)][:,0])
    saturday_fct = np.flip(forcst[int(forcst.shape[0]/7*5):int(forcst.shape[0]/7*6)][:,0])
    sunday_fct = np.flip(forcst[int(forcst.shape[0]/7*6):int(forcst.shape[0]/7*7)][:,0])
    
    week = [monday_fct,tuesday_fct,wednesday_fct,thursday_fct,friday_fct,saturday_fct,sunday_fct]
                 
    maximum = []
    for d in range(int(forcst.shape[0]/7)):
        maximum.append(np.ceil(max([monday_fct[d], tuesday_fct[d], wednesday_fct[d], thursday_fct[d], friday_fct[d]])))
    
    return [week,maximum]