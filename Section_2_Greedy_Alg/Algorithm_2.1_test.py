# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 14:43:51 2019

@author: apple
"""
import graph as G

g=G.Graph('directed')
data = [[7,1],[5,2],[9,3],[1,4],[8,5],[3,6],[8,6],[4,7],[9,7],[2,8],[6,9]]
for i in range(1,10):
    g.addVertex(i)
    
for d in data:
    g.addEdge(d[0],d[1])

size = g.SCC()
print(size)
##def DFS(self,how,key,s,checklist,lead,leadlist,timelist):   #key is idvalue of node
#checklist= []
#leadlist=[]
#lead = {}
#checklist.append(9)
#leadlist.append(9)
#
#for n in g.nodes[9].influx:  #Note: when backwarded this should be influx
#    if n not in checklist:
#        self.DFS(how,n.idvalue,s,checklist,lead,leadlist,timelist)
##t+=1
#timelist.append(key) #save the sorted order of
#
##lead_dict = g.SCC()