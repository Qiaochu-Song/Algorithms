# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 12:19:37 2019

@author: apple
"""
import graph as G
import pdb

import sys
 
sys.setrecursionlimit(100000)

f = open('SCC.txt','r')
g = G.Graph('directed')

for i in range(0,875714):
    g.addVertex(i+1)

for line in f: 
    line = line.rstrip('\t \n')
    line = list(line.split(' '))
    
    g.addEdge(int(line[0]),int(line[1]))   #convert each line into an empty vertex directly  

f.close()
leader = g.SCC()

#lead_dict = g.SCC()
