import graph as G
import numpy as np
import pdb

file = open('dijkstradata.txt', 'r')
graph = G.Graph(200)
for i in range(0, 200):
    graph.addVertex(i + 1)

for line in file:
    line = line.rstrip('\t\n')
    line = line.split('\t')
    i = 1
    while i < len(line):
        [a, b] = line[i].split(',')
        if a > line[0]:
            graph.addEdge(int(line[0]), int(a), int(b))
        i += 1

# up to here is all right

# Run BFS and set unconnected nodes to path=1000000
checklist = np.zeros(graph.size)
checklist = graph.BFS(checklist, 1)
for i in checklist:
    if i == 0:
        graph.nodes[i - 1].path = 1000000

# now in checklist, 1: connected, 0: unconnected
# as the checklist shows all reachable from No.1 node

graph.Dijkstra_SS()

outlist = []
for i in [7, 37, 59, 82, 99, 115, 133, 165, 188, 197]:
    outlist.append(graph.nodes[i - 1].path)
print(outlist)
