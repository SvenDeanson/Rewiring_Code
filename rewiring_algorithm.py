#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  3 16:19:11 2022

@author: sven
"""

import numpy as np
import networkx as nx
from tqdm import tqdm
from measure_frustration import frustration_count

def Rewiring(G0,n_iter,t_iter):

    total=[]
    for i in tqdm(range(n_iter)):
        
        H = G0.copy()
        
        res=[]
        res.append(frustration_count(H))

        for t in range(1,t_iter):
            
            nx.algorithms.connected_double_edge_swap(H, nswap=1) # THIS SHOULD BE FIXED
            
            fr = frustration_count(H)
            res.append(fr)

        total.append(res) 
        
    return np.array(total)