#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  3 16:16:32 2022

@author: sven
"""
import random
import numpy as np
from tqdm import tqdm
from measure_frustration import frustration_count,calculate_delta


def objective_func1(p,q):
    
    return np.sqrt((p[0]-q[0])**2+(p[1]-q[1])**2)

def objective_func2(p,q):
    
    return np.sqrt((p[0]-q[0])**2)

def random_neighbour(G):
 
    H = G.copy()
    
    random_node = random.sample(list(H.nodes()),1)[0]
    
    chosen_color = H.nodes[random_node]['color']
    if chosen_color == "Silver":
        H.nodes[random_node]['color'] = "Black"
    else:
        H.nodes[random_node]['color'] = "Silver"
    
    return H

def Simulated_Annealing_Track(target_f, target_d, g, n_iterations, step_size, temp, objective_func=objective_func2):
    
    best = g.copy()
    
    #y_true = np.array([len(g.edges()),0])
    y_true = np.array([target_f,target_d])
    y_best = np.array([frustration_count(best),calculate_delta(best)])
    
    best_eval = objective_func(y_best,y_true)

    curr, curr_eval = best, best_eval
    scores = list()
    states = list()
    
    for i in tqdm(range(n_iterations)):

        #candidate = curr + randn(len(bounds)) * step_size
        
        candidate = random_neighbour(curr.copy())
        
        y_candidate = np.array([frustration_count(candidate),calculate_delta(candidate)])

        candidate_eval = objective_func(y_candidate,y_true)
        
        if candidate_eval < best_eval:

            best, best_eval = candidate.copy(), candidate_eval

            scores.append(best_eval)
            states.append(best)

            print('>%d f(%s) = %.5f' % (i, best, best_eval))

        diff = candidate_eval - curr_eval

        t = temp / float(i + 1)

        metropolis = np.exp(-diff / t)

        if diff < 0 or np.random.randn() < metropolis:

            curr, curr_eval = candidate.copy(), candidate_eval

    return [best, best_eval, scores, states]

def Simulated_Annealing_Fast(target_f, target_d, g, n_iterations, step_size, temp, objective_func=objective_func2):
    
    best = g.copy()
    
    #y_true = np.array([len(g.edges()),0])
    y_true = np.array([target_f,target_d])
    y_best = np.array([frustration_count(best),calculate_delta(best)])
    
    best_eval = objective_func(y_best,y_true)

    curr, curr_eval = best, best_eval

    for i in tqdm(range(n_iterations)):

        #candidate = curr + randn(len(bounds)) * step_size
        
        candidate = random_neighbour(curr.copy())
        
        y_candidate = np.array([frustration_count(candidate),calculate_delta(candidate)])

        candidate_eval = objective_func(y_candidate,y_true)
        
        if candidate_eval < best_eval:

            best, best_eval = candidate.copy(), candidate_eval

        diff = candidate_eval - curr_eval

        t = temp / float(i + 1)

        metropolis = np.exp(-diff / t)

        if diff < 0 or np.random.randn() < metropolis:

            curr, curr_eval = candidate.copy(), candidate_eval

    return best