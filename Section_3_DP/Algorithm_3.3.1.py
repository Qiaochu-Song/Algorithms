import heapq
import pdb


class Character:
    def __init__(self, id, f):
        self.id = id
        self.child = []
        self.f = f
        self.rank1 = 0  # for longest code
        self.rank2 = 0  # for shortest code

    def __lt__(self, character2):
        return self.f < character2.f


clist = []
file = open('huffman.txt', 'r+')
i = -1
for line in file:
    if i == -1:
        i += 1
        continue
    line = line.rstrip('\t')
    freq = int(line)
    c = Character(i, freq)
    clist.append(c)
    i += 1
file.close()
# clist: a list of all characters with id = 0--999
# sort them with a heap
# data loaded correctly


def huffman(clist):
    heapq.heapify(clist)
    while len(clist) > 1:
        a = heapq.heappop(clist)
        b = heapq.heappop(clist)
        heapq.heappush(clist, merge(a, b))
    root = clist[0]
    return [root.rank1, root.rank2]


def merge(character1, character2):
    f = character1.f + character2.f
    new = Character(-1, f)  # set as a merger with id=-1
    new.child = [character1, character2]
    new.rank1 = 1 + max(character1.rank1, character2.rank1)
    new.rank2 = 1 + min(character1.rank2, character2.rank2)
    return new


result = huffman(clist)
print(result)
