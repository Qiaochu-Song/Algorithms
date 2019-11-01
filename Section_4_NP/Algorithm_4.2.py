import numpy as np
from itertools import combinations
from math import *
import pdb

file = open('tsp.txt', 'r+')
i = -1
for line in file:
    if i == -1:
        n = int(line.rstrip('\t'))
        coor = np.empty((n, 2))
        i += 1
    else:
        [x, y] = line.rstrip('\t').split(' ')
        coor[i][:] = np.array([x, y])
        i += 1
file.close()

# No.vertex is zero-based
# S is a subset of size m that contains start
# j in set S and j != 0
# use TWO 2D array to save the values in the current & last round

eu_dist = np.zeros((n, n))
for k in range(0, n):
    for j in range(0, n):
        if k == j:
            eu_dist[k][j] = 0
        else:
            eu_dist[k][j] = sqrt((coor[k][0] - coor[j][0]) ** 2 + (coor[k][1] - coor[j][1]) ** 2)

# for quick reference to the factorial value
lookup_f = np.zeros(n + 1)
for i in range(0, n + 1):
    lookup_f[i] = factorial(i)

# choose #i from #j, save number of combinations in a 2d array
comb_table = np.zeros((n + 1, n + 1))
for i in range(0, n + 1):
    for j in range(0, n + 1):
        if i > j:
            comb_table[i][j] = 0
        elif i == j:
            comb_table[i][j] = 1
        elif i < j:
            comb_table[i][j] = lookup_f[j] / (lookup_f[i] * lookup_f[j - i])


# calculate the combinatorial number of this combination set
# N = sum(comb(set[i-1], i)), i = 1 to len(set), set in ascending sorted order
def encode(s):  # intput is a tuple/list of combination
    N = 0
    for x, y in enumerate(s, start=1):  # x is 1-based index
        N += comb_table[x][y]
    return int(N)

# #******test******
# vertices = list(range(0, n))
# x = list(combinations(vertices, 3))
# code = []
# for i in x:
#     code.append(encode(i))
# print(max(code), min(code), len(code))
# ****************


# initialization
# max_size = maximum possible number of combinations
max_size = int(comb_table[12][25])
A = np.full((max_size, 25), np.inf)  # indexed by [# set][k]
A[0][0] = 0
cache = np.empty((max_size, 25))

vertices = list(range(1, n))  # other vertices except 0
for m in range(1, n):  # size of set {s1 - 0}
    print('%d /24 proceeding' % m)
    # passby = a set of s WITHOUT 0
    passby = list(combinations(vertices, m))
    for s1 in passby:
        s1 = [0] + list(s1)
        # now add 0 to the front of s
        s1_code = encode(s1)
        for j in s1:
            if j == 0:
                continue
            else:
                choice = []
                for k in s1:
                    if k != j:
                        if k == 0 and m != 1:
                            continue  # i.e. this candidate A[set, 0]=inf
                        else:
                            dist_jk = eu_dist[j][k]
                            s_j = s1.copy()
                            s_j.remove(j)
                            # pdb.set_trace()
                            s_j_code = encode(s_j)
                            candidate = A[s_j_code][k] + dist_jk
                            choice.append(candidate)
                    else:
                        continue
                cache[s1_code][j] = min(choice)
    A, cache = cache, A

print(s1, s1_code)

temp = []
a = A[0][:]
print(a)
for j in range(1, n):
    temp.append(a[j] + eu_dist[0][j])
print(min(temp))
