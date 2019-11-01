import numpy as np
import pdb
import custom_arr


class Vertex:
    def __init__(self, key):
        self.idvalue = key
        self.connection = []
        self.edge = custom_arr.Custom_Arr(itemtype=Edge)
        self.influx = {}   # other nodes that point to this node
        self.outflux = {}   # nodes that this nodes points to


class Edge:
    def __init__(self, tail, head, length):  # end is vertex id
        self.tail = tail
        self.head = head
        self.length = length
        self.score = 0


class DirectedGraph:
    def __init__(self, size):
        self.idlist = []
        self.size = size
        self.nodes = np.empty(size, dtype=Vertex)
        self.edges = custom_arr.Custom_Arr(itemtype=Edge)

    def addVertex(self, key):  # key: vertex name, i.e., idvalue
        self.nodes[key] = Vertex(key)  # g.nodes[ind] refer each vertex

    def addEdge(self, tail, head, length=1):  # for directed graph
        e = Edge(tail, head, length)
        self.edges.add(e)
        # pdb.set_trace()
        self.nodes[tail - 1].outflux[head - 1] = length
        self.nodes[head - 1].influx[tail - 1] = length


def load_graph(filename):
    file = open(filename, 'r+')
    i = 0
    for line in file:
        if i == 0:
            [n, m] = [int(r) for r in line.rstrip('\t').split(' ')]
            graph = DirectedGraph(n)
            for j in range(0, n):
                graph.addVertex(j)
            i += 1
        else:
            [tail, head, length] = line.rstrip('\t').split(' ')
            graph.addEdge(int(tail), int(head), int(length))
    file.close()
    return graph, n, m


def BellmanFord(graph, n, m, source=1):
    A = np.full(n, np.inf)  # initialization
    A[source - 1] = 0
    cache = np.empty(n)
    for i in range(0, n):  # add 1 more loop for negative cycle check
        for v in range(0, n):  # for each node
            case_2 = []
            for w, length in graph.nodes[v].influx.items():
                case_2.append(A[w.idvalue - 1] + length)
            cache[v] = min(A[v], min(case_2))
        cache, A = A, cache
    # negative cycle check, now A is the final round A[n,v], cache is A[n-1,v]
    if sum(cache - A) != 0:
        print('Negative cycle detected!')
    else:
        print('No negative cycle detected.')
    return


def FloydWarshall(graph, n):
    A = np.full((n, n, n), np.inf)
    for i in range(0, n):
        A[i][i][0] = 0
        for j, length in graph.nodes[i].influx.items():
            # here j in 0-indexing
            # pdb.set_trace()
            A[i][j][0] = length
            # print(i, j, A[i][j][0])
    for k in range(1, n):
        if k % 200 == 0:
            print('%.2f percent complete' % (k / 1000))
        for i in range(0, n):
            for j in range(0, n):
                A[i][j][k] = min(A[i][j][k - 1], A[i][k][k - 1] + A[k][j][k - 1])
                # pdb.set_trace()
    # check if there exists a negative cycle
    flag = 0
    for i in range(0, n):
        if A[i][i][n - 1] < 0:
            print('Negative cycle detected!')
            flag = 1
            break
    if flag == 0:
        print(np.min(A[:, :, n - 1]))
    return


# def Johnson(graph)


filelist = ['g1.txt', 'g2.txt', 'g3.txt']
for f in filelist:
    graph, n, m = load_graph(f)
    print('graph %s loaded' % f)
    FloydWarshall(graph, n)
    print('graph %s caculated' % f)
