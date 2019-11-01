import numpy as np
import custom_arr as arr


class HashTable():
    def __init__(self, size=1000000):
        self.data = np.empty(size, dtype=np.object)
        self.size = 0
        for i in range(0, size):
            self.data[i] = []

    def __getitem__(self, index):
        return self.data[index]

    def __setitem__(self, index, item):
        self.data[index] = item

    def hf(self, item):
        temp = item
        if item < 0:
            temp = 0 - item
        loc = (temp + temp % 17) % 999983
        return loc

    def insert(self, item):
        loc = self.hf(item)
        self[loc].append(item)
        self.size += 1

    def lookup(self, item):
        loc = self.hf(item)
        for i in self[loc]:
            if i == item:
                return True
        return False
