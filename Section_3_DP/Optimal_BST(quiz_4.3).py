import numpy as np

# freq = np.array([0.05, 0.4, 0.08, 0.04, 0.1, 0.1, 0.23])
freq = np.array([0.2, 0.05, 0.17, 0.1, 0.2, 0.03, 0.25])
A = np.zeros((7, 7))

# optimal binary search tree
for s in range(0, 7):
    for i in range(0, 7-s):
        caselist = []
        sumfreq = sum(freq[i:i + s + 1])
        for r in range(i, i + s + 1):
            if r + 1 > i + s:
                b = 0
            else:
                b = A[r + 1][i + s]
            if i > r - 1: 
                a = 0
            else: 
                a = A[i][r - 1]
            caselist.append(a + b)
        A[i][i + s] = sumfreq + min(caselist)
print(A)
