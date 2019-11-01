import numpy as np

file = open('jobs.txt', 'r')
j_weight = np.empty(10000)
j_length = np.empty(10000)
i = -1
for line in file:
    if i == -1:
        i += 1
        continue
    line.rstrip('\n')
    [weight, length] = line.split(' ')
    j_weight[i] = int(weight)
    j_length[i] = int(length)
    i += 1
# sort in decreasing order of (w-l),arbitrary ties
# calculate sum w*l
print(i)


class Job():
    def __init__(self, id):
        self.length = j_length[id]
        self.weight = j_weight[id]
        self.score1 = self.weight - self.length
        self.score2 = self.weight / self.length
        self.complete_t = -1
        # self.flag = 0


def method1(j):
    return (j.score1, j.weight)


def method2(j):
    return j.score2


class Schedule():
    def __init__(self, size=10000):
        self.seq = []
        for i in range(0, 10000):
            job = Job(i)
            self.seq.append(job)

    def reschedule(self, method):
        self.seq.sort(key=method, reverse=True)
        # in descending order
        t = 0
        sum = 0
        for i in self.seq:
            t = t + i.length
            i.complete_t = t
            sum = sum + i.complete_t * i.weight
        print(sum)


sd = Schedule()
sd.reschedule(method1)
sd.reschedule(method2)
# output: method1: 69120882574, method2: 67311454237
