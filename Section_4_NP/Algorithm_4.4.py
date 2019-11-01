import numpy as np
# import random
import custom_arr
import pdb
# import resource
# import sys

# sys.setrecursionlimit(10 ** 6)
# resource.setrlimit(resource.RLIMIT_STACK, (2 ** 29, 2 ** 30))


class Vertex:
    def __init__(self, key):
        self.idvalue = key
        self.connection = []
        self.edge = custom_arr.Custom_Arr(itemtype=Edge)
        self.influx = []   # other nodes that point to this node
        self.outflux = []   # nodes that this nodes points to
        self.path = 0
        self.leader = key

    def addneighbors(self, vertices):
        # here 'vertices' is a list of vertex objs
        for i in vertices:
            self.connection.append(i)


class Edge:
    def __init__(self, end1, end2, length):  # end is vertex id
        self.end1 = end1
        self.end2 = end2
        self.length = length
        self.score = 0


class Graph:
    def __init__(self, size, graphtype='undirected'):  # undirected by default
        self.idlist = []
        self.size = 0
        self.checklist = np.zeros(self.size)
        self.timelist = []
        self.nodes = np.empty(size, dtype=Vertex)
        self.edges = custom_arr.Custom_Arr(itemtype=Edge)
        if graphtype == 'directed':
            self.Gtype = 'D'
        if graphtype == 'undirected':
            self.Gtype = 'U'

    def addVertex(self, key):  # key: vertex name, i.e., idvalue
        self.idlist.append(key)
        self.nodes[key - 1] = Vertex(key)  # g.nodes[ind] refer each vertex
        self.size += 1

    def addEdge(self, tail, head, edge=1):
        if self.Gtype == 'U':  # Note: the index in array g.nodes is idvalue-1
            # how to avoid repeated edges in one node??
            self.nodes[tail - 1].connection.append(self.nodes[head - 1])
            self.nodes[head - 1].connection.append(self.nodes[tail - 1])
            newedge = Edge(tail, head, edge)
            self.edges.add(newedge)
            self.nodes[tail - 1].edge.add(newedge)
            self.nodes[head - 1].edge.add(newedge)

        if self.Gtype == "D":
            self.nodes[tail - 1].outflux.append(self.nodes[head - 1])
            self.nodes[head - 1].influx.append(self.nodes[tail - 1])

    def DFS(self, how, key, leadsize, leadflag=None):
        # leadflag = the current leader during this loop
        # key is idvalue of node
        self.checklist[key - 1] = 1
        # WARNING: make sure the lists in lead list is correct.
        if how == 'forward':
            for node in self.nodes[key - 1].outflux:
                if self.checklist[node.idvalue - 1] == 0:
                    # Note: n is storage of node, not idvalue
                    leadsize += 1
                    # to mark nodes with its leader
                    node.leader = leadflag
                    leadsize = self.DFS(how, node.idvalue, leadsize, leadflag)
                else:
                    continue
                    # print(leadsize)
            return leadsize

        elif how == 'backward':
            for node in self.nodes[key - 1].influx:
                if self.checklist[node.idvalue - 1] == 0:
                    self.DFS(how, node.idvalue, leadsize)
            self.timelist.append(key)
            # print(len(self.timelist))  # for debug
            # save sorted order of nodes according
            # to finishing time (max to min)

    def DFS_loop(self, how='backward'):
        # t = 0   #keep track of finishing time in the 1st pass
        # s = 0  # keep track of the key of leadsize in final lead list
        self.checklist = np.zeros(self.size)
        lead = []
        leadsize = 1  # the node itself
        # use timelist instead of t to keep track of finishing time in 1st pass
        if how == 'backward':
            # pdb.set_trace()
            for i in range(1, self.size + 1):
                #  NOTE: i is idvalue,use i-1 when indexing checklist array
                if self.checklist[i - 1] == 0:
                    self.DFS(how, i, leadsize)
            # print(timelist)
            return

        elif how == 'forward':
            for i in self.timelist[::-1]:  # reverse to get descending finishing time order
                if self.checklist[i - 1] == 0:
                    leadsize = 1
                    leadflag = i
                    sccsize = self.DFS(how, i, leadsize, leadflag)
                    # print(sccsize)  # ERROR, sccsize = None
                    lead.append(sccsize)
            return lead

    def SCC(self):
        if self.Gtype == 'U':    # only for directed graph
            print('the graph is undirected')
            raise TypeError
        else:
            self.DFS_loop('backward')
            SCCsize = self.DFS_loop('forward')
        return SCCsize   # a list of each SCC size

def filetograph(filename):
    file = open(filename, 'r')
    i = -1
    for line in file:
        if i == -1:
            n = int(line.rstrip('\t'))
            g = Graph(2 * n, 'directed')
            for j in range(1, 2 * n + 1):
                g.addVertex(j)
            i += 1
        else:
            # each row of array 'clause' is a clause, with 'or'
            [x, y] = line.rstrip('\t').split(' ')
            x = int(x)
            y = int(y)
            logic_edge(g, n, x, y)
    file.close()
    return g, n


def logic_edge(g, n, x, y):
    # NOTE that addEdge takes two parameters, tail, head, both are 1-indexed
    if x > 0 and y > 0:
        # if x is F then y must be T, if y is F then x must be T
        g.addEdge(x + n, y)
        # x + n indicates the case where variable[x] is false
        g.addEdge(y + n, x)
    elif x < 0 and y < 0:
        # if x is T then y must be F, if y is T then x must be F
        g.addEdge(-x, -y + n)
        g.addEdge(-y, -x + n)
    elif x < 0 and y > 0:
        # if x is T then y must be T, if y is F then x must be F
        g.addEdge(-x, y)
        g.addEdge(y + n, -x + n)
    elif x > 0 and y < 0:
        # if x is F then y must be F, if y is T then x must be T
        g.addEdge(x + n, -y + n)
        g.addEdge(-y, x)


# ******test SCC*******
# g1 = Graph(9, 'directed')
# data = [[7,1],[5,2],[9,3],[1,4],[8,5],[3,6],[8,6],[4,7],[9,7],[2,8],[6,9]]
# for i in range(1, 10):
#     g1.addVertex(i)

# for d in data:
#     g1.addEdge(d[0], d[1])

# size = g1.SCC()
# print(size)
# for i in range(0, 9):
#     print(g1.nodes[i].leader)
# **********************


# *******test 2sat*******
g, n = filetograph('test.txt')
g.SCC()
for i in range(0, n):
    if g.nodes[i].leader == g.nodes[i + n].leader:
        print('2sat cannot be satisfied!')
        break
# this test 2sat is satisfiable
# ********

for i in range(1, 7):
    filename = '2sat' + str(i) + '.txt'
    g, n = filetograph(filename)
    print('file %d converted to graph.' % i)
    g.SCC()
    for i in range(0, n):
        if g.nodes[i].leader == g.nodes[i + n].leader:
            print('2sat cannot be satisfied!')
            break
# result 101100


# Papadilitrious local search algorithm
# def loadfile(filename):
#     file = open(filename, 'r')
#     i = -1
#     for line in file:
#         if i == -1:
#             n = int(line.rstrip('\t'))
#             clause = np.zeros((n, 2))
#             i += 1
#         else:
#             # each row of array 'clause' is a clause, with 'or'
#             [x, y] = line.rstrip('\t').split(' ')
#             clause[i][:] = np.array([x, y])
#     file.close()
#     return clause, n


# def preprocess(clause):
#     n = len(clause)
#     boolarray = np.empty(n, bool)
#     pos = np.empty(n, bool)
#     neg = np.empty(n, bool)
#     union = set()  # elements need to be settled recursively
#     for i in range(0, n):
#         (x, y) = clause[i][:]
#         if x > 0:
#             pos[x - 1] = True
#         else:
#             neg[-x - 1] = True
#         if y > 0:
#             pos[y - 1] = True
#         else:
#             neg[-y - 1] = True
#     for i in range(0, n):
#         if pos[i] is True:
#             if neg[i] is None:
#                 boolarray[i] = True
#             elif neg[i] is True:
#                 union.add(i)  # 0-based indexing
#         if pos[i] is None:
#             # it is ok to set as false, no matter neg[i] is true or none
#             boolarray[i] = False
#         # initialize the undetermined elements in the boolean array
#     # only random init the reduced smaller set, i.e. less recursion
#     for i in union:
#         boolarray[i] = bool(random.getrandbits(1))
#         # this way is faster than random.choice([True, False])
#     # return a rationally initialized array and "union"
#     return boolarray, union


# def preprocess(clause):
#     n = len(clause)
#     boolarray = np.empty(n, bool)
#     pos = set()
#     neg = set()
#     for i in range(0, n):
#         (x, y) = clause[i][:]
#         if x > 0:
#             pos.add(x)
#         else:
#             neg.add(-x)
#         if y > 0:
#             pos.add(y)
#         else:
#             neg.add(-y)
#     set_true = pos - neg
#     set_false = neg - pos
#     for
#     # elements only in pos or only in neg
#     pos.symmetric_difference(neg)


# def judge_adjust(x, y, A):
#     # A is the boolarray; x, y are indices of boolarray
#     # only judge and adjust clause containing elements in union
#     # adapt to zero-based indexing
#     if x < 0:
#         x = -x - 1
#         if y < 0:
#             y = -y - 1
#             output = not(A[x]) or not(A[y])
#         else:
#             y = y - 1
#             output = not(A[x]) or A[y]
#     elif x > 0:
#         x = x - 1
#         if y > 0:
#             y = y - 1
#             output = A[x] or A[y]
#         else:
#             y = -y - 1
#             output = A[x] or not(A[y])
#     if output is True:
#         return True
#     else:
#         A[x] = not(A[x])  # flip
#         return False


# def twosat(clause, boolarray, union):
#     # do greedy local search algorithm
#     n = len(clause)
#     t = 0
#     while t < n ** 2:
#         t += 1
#         for i in range(0, n):
#             x, y = clause[i][0], clause[i][1]
#             if (abs(x) - 1) in union or (abs(y) - 1) in union:
#                 if judge_adjust(x, y, boolarray) is False:
#                     choice = np.random.randint(0, 2)
#                     if choice == 0:
#                         boolarray[x] = not(boolarray[x])
#                     else:
#                         boolarray[y] = not(boolarray[y])
