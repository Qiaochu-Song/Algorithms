import hashtable as h
import custom_arr as ca
import pdb

file = open('2sum.txt', 'r')
ht = h.HashTable(1000000)
data = ca.Custom_Arr(itemtype=int)


for line in file:
    line.rsplit('\t')
    line = int(line)
    data.add(line)
    ht.insert(line)
# there might be some repititions in data!
file.close()
print('data loaded')


def twosum(data, ht):
    count = 0
    for t in range(-10000, 10001):
        for i in data:
            if (t - i) != i:
                if ht.lookup(t - i) is True:
                    count += 1
                    break
    return count


# *******TEST*******
# for i in range(1000, 1050):
#     ht.insert(i)
# print(ht.lookup(1020))
# d = range(1000, 1050)
# print(twosum(d, ht))
# ******************

print(twosum(data, ht))
