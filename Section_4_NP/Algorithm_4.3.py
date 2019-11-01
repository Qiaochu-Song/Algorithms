import numpy as np
from math import *
import pdb

file = open('nn.txt', 'r')
i = -1
for line in file:
    if i == -1:
        n = int(line.rstrip('\t'))
        coor = np.zeros((n, 2))
        i += 1
    else:
        [x, y] = line.rstrip('\t').split(' ')[1:]
        coor[i][:] = np.array([x, y])
        i += 1
file.close()


def eu_square(id1, id2):
    return (coor[id1][0] - coor[id2][0]) ** 2 + (coor[id1][1] - coor[id2][1]) ** 2


def tsp_heuristic(coor):
    n = len(coor)
    flag = np.zeros(n)  # indicate visit state of each city
    current = 0
    count = 1
    triplen = 0
    while count != n:
        candidate = np.inf
        next = 0
        for i in range(1, n):
            if flag[i] == 0:
                d_sq = eu_square(current, i)
                if d_sq < candidate:
                    candidate = d_sq
                    next = i
        flag[next] = 1  # mark 'next' as visited
        triplen += sqrt(candidate)  # calculate new trip length
        current = next  # set 'next' as new start
        count += 1  # add one to the count of cities visited
        if count % 2000 == 0:
            print ('%d out of 33708 complete' % count)
    # final hop: return to the original city
    triplen += sqrt(eu_square(0, current))
    return triplen


print(tsp_heuristic(coor))
