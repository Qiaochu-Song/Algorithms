import graph as G
import numpy as np
import heapq
import pdb

file = open('edges.txt', 'r')
graph = G.Graph(500)
for i in range(0, 500):
    graph.addVertex(i + 1)

i = -1
for line in file:
    if i == -1:
        i += 1
        continue
    line = line.rstrip('\n')
    [n1, n2, l] = line.split(' ')
    graph.addEdge(int(n1), int(n2), int(l))
    i += 1
print(n1, n2, l)

graph.MST()
