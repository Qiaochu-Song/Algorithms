
import numpy as np
import graph as G
import pdb

g = G.Graph(500)
for i in range(1, 501):
    g.addVertex(i)

file = open('clustering.txt', 'r')
i = -1
for line in file:
    if i == -1:
        i += 1
        continue
    line.rstrip('\n')
    [n1, n2, length] = line.split(' ')
    g.addEdge(int(n1), int(n2), int(length))
    # use g.edges to get the custom_arr of edges
    i += 1
sortedEdge = g.edges[0:g.edges.size]
sortedEdge = sorted(sortedEdge, key=lambda x: (x.length, x.end1, x.end2))
# for i in range(0, 100):
#    print(sortedEdge[i].length)
# in sortedEdge, edges are in length ascending order


def clustering(sortedEdge, k=4):
    ufs = UFS()
    spacedict = {}
    for e in sortedEdge:
        if len(ufs.group) > 4:
            ufs.union(e.end1, e.end2)
        else:
            a = ufs.find(e.end1)
            b = ufs.find(e.end2)
            if a != b:
                k = (max(a, b), min(a, b))
                if k in spacedict.keys():
                    spacedict[k] = min(spacedict[k], e.length)
                else:
                    spacedict.update({k: e.length})
    return ufs, spacedict


class UFS():
    def __init__(self, size=500):
        self.size = size
        self.leader = dict(zip(range(1, size + 1), range(1, size + 1)))
        self.group = dict([(x, [x]) for x in range(1, size + 1)])

    def find(self, key):
        return self.leader[key]

    def union(self, key1, key2):
        l1 = self.find(key1)
        l2 = self.find(key2)
        if l1 != l2:
            if len(self.group[l1]) <= len(self.group[l2]):
                for i in self.group[l1]:
                    self.leader[i] = l2
                    self.group[l2].append(i)
                del self.group[l1]
            else:
                for i in self.group[l2]:
                    self.leader[i] = l1
                    self.group[l1].append(i)
                del self.group[l2]


ufs, spacedict = clustering(sortedEdge)
# pdb.set_trace()
print(spacedict)
# ufstest = UFS(5)
# ufstest.union(1, 2)
# pdb.set_trace()
# print(ufstest.group)
