from datetime import datetime

today = str(datetime.today().date())

print(f"Today is{today}")

import string
import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from kagome_generator import *

def Create_Triangular_Graph(n):
    p=[]
    for j in range(1,n+1):
        for i in range(1,n+1):
            p.append((j%2 + 2*i - 3, 2*j-2))
    
    points = p
    N = len(points)
    points = sorted(points,key=lambda l:l[1])
    
    g = nx.Graph()
    
    g.add_nodes_from(points)
    
    dic={}  
    for n,(x,y) in zip(g.nodes(),points):
        dic[n] = (x,y)

    for a,b in g.nodes():
        if (a+1,b+2) in g.nodes():
            g.add_edge((a,b),(a+1,b+2))
        if (a-1,b+2) in g.nodes():
            g.add_edge((a,b),(a-1,b+2))
        if (a+2,b) in g.nodes():
            g.add_edge((a,b),(a+2,b))

    return g

def Create_Random_Colored_Graph(n,choice,k=False):
    
    #############################################################
    # Choose network structure #
    #############################################################
    
    if choice==1:
        G = nx.grid_2d_graph(n,n)
    if choice==2:
        G = nx.triangular_lattice_graph(n,n)
    if choice==3:
        G = nx.path_graph(n)
        
    if choice==4:
        G = Create_Triangular_Graph(n)
        
    if choice==5:
        G =  Create_Kagome_Graph(n,n,plot=False)

    #############################################################
    # Color nodes #
    #############################################################
    
    N = len(G.nodes())
    
    if type(k) == bool:
        m = random.randrange(0,N)
        n = N-m
    else:
        m=int(round(k*N))
        n=int(round((1-k)*N))

    a = np.ones(N)
    a[:m] = -1
    np.random.shuffle(a)
    
    node_colors=[]
    for i in a:
        if i==1:
            node_colors.append("Silver")
        else:
            node_colors.append("Black")

    attr = {}
    for (node,value),color in zip(G.nodes.data(),node_colors):
        attr[node]=color

    nx.set_node_attributes(G, attr, 'color')
    
    #############################################################
    # Color edges #
    #############################################################
    
    N = len(G.edges())
    l = 1.0
    
    m=int(round(l*N))
    n=int(round((1-l)*N))

    a = np.ones(n+m)
    a[:m] = -1
    np.random.shuffle(a)
    
    dic={}
    for e,value in zip(G.edges(),a):
        dic[e] = value
    
    nx.set_edge_attributes(G, dic,'weight')
    
    #############################################################
    
    return G