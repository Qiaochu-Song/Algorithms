import numpy as np
import pdb

file = open('knapsack1.txt', 'r')
i = -1
weight = np.empty(100)
value = np.empty(100)
cache = np.zeros(10001)
A = np.empty(10001)
for line in file:
    if i == -1:
        i += 1
        continue
    a, b = line.rstrip('\t').split(' ')
    value[i], weight[i] = int(a), int(b)
    i += 1
file.close()
pdb.set_trace()
for i in range(0, 100):
    for x in range(0, 10001):
        ind = x - weight[i]
        if ind < 0:
            A[x] = cache[x]
        else:
            # pdb.set_trace()
            A[x] = max(cache[x], cache[int(ind)] + value[i])
    cache, A = A, cache

print(cache[-1])
