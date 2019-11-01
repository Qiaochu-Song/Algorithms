import numpy as np
import graph as g


class Custom_Arr():
    # an array appendable and with customized element, default 100
    def __init__(self, itemtype, capacity=100):
        self.data = np.empty(capacity, dtype=itemtype)
        self.capacity = capacity
        self.size = 0
        self.itemtype = itemtype

    def add(self, v):  # add a vertex v
        if self.size == self.capacity:
            self.capacity *= 4
            newdata = np.empty(self.capacity, dtype=self.itemtype)
            newdata[:self.size] = self.data
            self.data = newdata
        self.data[self.size] = v
        self.size += 1
