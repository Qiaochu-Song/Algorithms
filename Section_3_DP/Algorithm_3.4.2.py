import numpy as np
# import pdb

file = open('knapsack_big.txt', 'r')
i = -1
weight = np.empty(2000)
value = np.empty(2000)
cache = np.zeros(2000001)
A = np.empty(2000001)
for line in file:
    if i == -1:
        i += 1
        continue
    a, b = line.rstrip('\t').split(' ')
    value[i], weight[i] = int(a), int(b)
    i += 1
file.close()

for i in range(0, 2000):
    for x in range(0, 2000001):
        ind = int(x - weight[i])
        if ind < 0:
            A[x] = cache[x]
        else:
            # pdb.set_trace()
            A[x] = max(cache[x], cache[ind] + value[i])
    cache, A = A, cache
    if i % 100 == 0:
        print('process +5%')
print(cache[-1])
#ans = 4243395
