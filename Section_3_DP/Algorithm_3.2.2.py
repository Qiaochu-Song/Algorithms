from networkx.utils.union_find import UnionFind
import pdb

file = open('clustering_big.txt', 'r')
i = -1
hamming = {}
id_code = {}
for line in file:
    i += 1
    if i == 0:
        continue
    line = line.rstrip(' \n')
    line = line.replace(' ', '')
    code = int(line, 2)
    try:
        hamming[code].append(i)
    except KeyError:
        hamming.update({code: [i]})
    id_code.update({i: code})
    # to deal with repeated codes, use list as values in "hamming" dict
file.close()
# hamming is a dict with node_code: node_id pairs

# Create an array of bit-masks for the distances, using bit-shifts
mask1 = [1 << t for t in range(0, 24)]
mask2 = [1 << i | 1 << j for i in range(0, 24) for j in range(i + 1, 24)]
mask = mask1 + mask2
# the mask is right
# use ^ (i.e. xor) to apply mask to codes, changing each digit

# initialize all UnionFind sets
ufs = UnionFind(list(range(1, 200001)))
# for each node, search if its neighbors exist and union two sets
for i in range(1, 200001):
    synvalue = hamming[id_code[i]]
    if len(synvalue) > 1:
        for j in synvalue:
            if j != i:
                ufs.union(i, j)
    for m in mask:
        # find if such neighbor(s) exist (and list the ids)
        try:
            neighbor = hamming[id_code[i] ^ m]
        except KeyError:
            continue
        else:
            for n in neighbor:
                ufs.union(i, n)

pdb.set_trace()
# get final leaders in the UFS, then count the final number cluster
cluster_leaders = set([ufs[x] for x in range(1, 200001)])
# set is implemented with mapping, so the search operation is O(1) on average
# The number of clusters
num_clusters = len(cluster_leaders)
print(num_clusters)
