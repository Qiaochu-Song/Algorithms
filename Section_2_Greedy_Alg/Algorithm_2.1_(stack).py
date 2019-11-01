


num_nodes = 875715

# Adjacency representations of the graph and reverse graph
gr = [[] for i in range(num_nodes)]
r_gr = [[] for i in range(num_nodes)]

# The list index represents the node. If node i is unvisited then visited[i] == False and vice versa
visited = [False] * num_nodes

# The list below holds info about sccs. The index is the scc leader and the value is the size of the scc.
scc = [0] * num_nodes

stack = []  # Stack (LIFO) for DFS
order = []  # The finishing orders after the first pass

# read data

file = open("SCC.txt", "r")
data = file.readlines()

for line in data:
    items = line.split()
    gr[int(items[0])] += [int(items[1])]
    r_gr[int(items[1])] += [int(items[0])]

file.close()

# DFS on reverse graph　　 

for node in range(num_nodes):
    if visited[node] is False:
        stack.append(node)
        visited[node] = True
    while stack:
        stack_node = stack[-1]  # pop out the first element
        # visited[stack_node] = True    not sure about when to mark explored
        flag = 0
        for head in r_gr[stack_node]:  # if head unexplored, add to stack
            if visited[head] is False:
                flag = 1
                visited[head] = True
                stack.append(head)
        if flag == 0:  # i.e. all heads in stack_node are visited
            order.append(stack.pop())


# DFS on original graph

visited = [False] * len(visited)  # Resetting the visited variable
order.reverse()  # The nodes should be visited in reverse finishing times

for node in order:
    if visited[node] is False:
        stack.append(node)
        visited[node] = True
        scc[node] += 1  # set leader, include the "node" itself
    while stack:
        stack_node = stack[-1]
        flag = 0
        for tail in gr[stack_node]:
            if visited[tail] is False:
                flag = 1
                visited[tail] = True
                scc[node] += 1  # the index is node or stack_node
                stack.append(tail)
        if flag == 0:
            stack.pop()

# Getting the five biggest sccs
scc.sort(reverse=True)
print(scc[:5])
