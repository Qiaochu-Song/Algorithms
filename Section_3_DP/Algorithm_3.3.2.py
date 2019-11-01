import numpy as np
import pdb

path = []
file = open('mwis.txt', 'r+')
i = -1
for line in file:
    if i == -1:
        i += 1
        continue
    line = line.rstrip('\t')
    path.append(int(line))
file.close()
# load weight sequence of the path into a list

wis_cache = np.empty(1001)


def wis_loop():
    wis_cache[0] = 0
    wis_cache[1] = path[0]
    for i in range(2, 1001):
        a = path[i - 1] + wis_cache[i - 2]
        b = wis_cache[i - 1]
        wis_cache[i] = max(a, b)


def reconstruct():
    wiset = np.zeros(1001)
    i = 1000
    while i >= 1:
        if wis_cache[i - 1] >= wis_cache[i - 2] + path[i - 1]:
            i -= 1
            continue
        else:
            wiset[i] = 1
            i = i - 2
    return wiset


wis_loop()
wiset = reconstruct()
for i in [1, 2, 3, 4, 17, 117, 517, 997]:
    print(wiset[i])
