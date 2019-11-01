import numpy as np
import custom_arr
import heapq
import pdb


class Vertex:
    def __init__(self, key):
        self.idvalue = key
        self.connection = []
        self.edge = custom_arr.Custom_Arr(itemtype=Edge)
        self.influx = []   # other nodes that point to this node
        self.outflux = []   # nodes that this nodes points to
        self.path = 0

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


class PriorityQ():
    def __init__(self):
        self._queue = []
        self.size = 0
        self.order = 1

    def push(self, edge):
        heapq.heappush(self._queue, (edge.score, self.order, edge))
        self.order += 1
        # heapq.heappush(heap, item)
        # ERROR when pushing 104-127 (l = 561, score =2551) edge:
        # the edge was added into self._queue, but not correctly sifted
        # maybe it has the same value with its parent
        # (there is another edge with the same score in heap)
        self.size += 1

    def pop(self):   # return the min-scored edge)
        self.size = self.size - 1
        return heapq.heappop(self._queue)[-1]

    def delete(self, ind):
        self._queue[ind], self._queue[-1] = self._queue[-1], self._queue[ind]
        self._queue.pop()
        self.size = self.size - 1
        heapq.heapify(self._queue)


class Graph:
    def __init__(self, size, graphtype='undirected'):  # undirected by default
        self.idlist = []
        self.size = 0
        self.checklist = np.zeros(self.size)
        self.timelist = []
        self.nodes = np.empty(500, dtype=Vertex)
        self.edges = custom_arr.Custom_Arr(itemtype=Edge)  # use ".data" to look up in the array
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

    def Dijkstra_SS(self, source=1):
        # set source
        self.nodes[source - 1].path = 0
        check = np.zeros(self.size)
        edgeheap = PriorityQ()

        self.Dijkstra_loop(edgeheap, source, check)

    def Dijkstra_loop(self, edgeheap, node_id, check):
        # add node_id to X, i.e. mark as checked
        check[node_id - 1] = 1
        edgeset = self.nodes[node_id - 1].edge
        # add edges of node_id to heap, if the other end not checked
        for e in edgeset.data[:edgeset.size]:
            # custom_arr: Vertex.edge need '.data' when iterating
            if (check[e.end1 - 1] != 1) or (check[e.end2 - 1] != 1):
                e.score = e.length + self.nodes[node_id - 1].path
                edgeheap.push(e)

        if sum(check) == 200:
            return
        # pop the min-path edge from heap, if both ends UNchecked
        while True:
            choose_edge = edgeheap.pop()
            # print(choose_edge.end1, choose_edge.end2)
            if check[choose_edge.end1 - 1] != 1 or check[choose_edge.end2 - 1] != 1:
                break  # if the chosen edge not in X

        if check[choose_edge.end2 - 1] == 0:
            choose_node = self.nodes[choose_edge.end2 - 1]
        else:
            choose_node = self.nodes[choose_edge.end1 - 1]
        choose_node.path = choose_edge.score
        # print(choose_node.idvalue)
        # pdb.set_trace()
        self.Dijkstra_loop(edgeheap, choose_node.idvalue, check)

    def BFS(self, checklist, ind=1):
        for nd in self.nodes[ind - 1].connection:
            if checklist[nd.idvalue - 1] == 0:
                checklist[nd.idvalue - 1] = 1
                self.BFS(checklist, nd.idvalue)
        return checklist

    def DFS(self, how, key, leadsize):
        # key is idvalue of node
        self.checklist[key - 1] = 1  # key is idvalue
        # pdb.set_trace()

        print('key' + str(key))

        # WARNING: make sure the lists in lead list is correct.
        if how == 'forward':
            for node in self.nodes[key - 1].outflux:
                if self.checklist[node.idvalue - 1] == 0:
                    # Note: n is storage of node, not idvalue
                    leadsize += 1
                    leadsize = self.DFS(how, node.idvalue, leadsize)
                else:
                    continue
                    # print(leadsize)
            return leadsize

        elif how == 'backward':
            for node in self.nodes[key - 1].influx:
                if self.checklist[node.idvalue - 1] == 0:
                    self.DFS(how, node.idvalue, leadsize)
            self.timelist.append(key)
            print(len(self.timelist))  # for debug
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
            for i in self.timelist:
                if self.checklist[i - 1] == 0:
                    leadsize = 1
                    sccsize = self.DFS(how, i, leadsize)
                    print(sccsize)  # ERROR, sccsize = None
                    lead.append(sccsize)
            return lead

    def SCC(self):
        if self.Gtype == 'U':    # only for directed graph
            print('the graph is undirected')
            raise TypeError
        else:
            timeline = self.DFS_loop('backward')
            SCCsize = self.DFS_loop('forward')
        return SCCsize   # a list of each SCC size

    def copy(self):
        _g = Graph()
        _g.idlist = self.idlist.copy()
        _g.nodes = self.nodes.copy()
        _g.size = self.size
        return _g

    def MST(self, source=1):
        # set source
        self.nodes[source - 1].path = 0
        check = np.zeros(self.size)
        edgeheap = PriorityQ()
        total = 0
        self.MST_loop(edgeheap, source, check, total)

    def MST_loop(self, edgeheap, node_id, check, total):
        # add node_id to X, i.e. mark as checked
        check[node_id - 1] = 1
        edgeset = self.nodes[node_id - 1].edge
        # stop loop iteration if the last node sucked into X
        if sum(check) == 500:
            print(total)
            return
        # add edges of node_id to heap, if the other end unchecked
        for e in edgeset[:edgeset.size]:
            if (check[e.end1 - 1] != 1) or (check[e.end2 - 1] != 1):
                e.score = e.length
                # in MST, score is edge length, not path+edge
                edgeheap.push(e)

        # pop the min-path edge from heap, if both ends UNchecked
        while True:
            choose_edge = edgeheap.pop()
            # print(choose_edge.end1, choose_edge.end2)
            if check[choose_edge.end1 - 1] != 1 or check[choose_edge.end2 - 1] != 1:
                break  # if the chosen edge not in X

        if check[choose_edge.end2 - 1] == 0:
            choose_node = self.nodes[choose_edge.end2 - 1]
        else:
            choose_node = self.nodes[choose_edge.end1 - 1]
        total = total + choose_edge.score
        # and if necessary, also create an list of all selecte edges in MST
        # mst = []    mst.append(choose_edge)
        # and include list mst in params of both functions
        # print(choose_node.idvalue)s
        # pdb.set_trace()
        # print(total)
        self.MST_loop(edgeheap, choose_node.idvalue, check, total)
