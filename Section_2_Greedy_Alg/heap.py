# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 18:16:14 2019

@author: apple
"""
import numpy as np
import graph as G

class Heapedges:
    def__init__(self,size=10):
        self.elements = arr.Custom_Arr(size, dtype=G.Edge)
        self.size = 0

    def addedge(self, edge):
        self.elements.add(edge)
        self.size = self.elements.size
        self.shiftup(self.size - 1)
    
    def extract(self, ind=0):
        # use for push out the min root (ind=0) and update some elements
        extraction = self.elements[ind]
        self.elements[ind] = self.elements[-1]
        # move the last one to the extract place and shiftdown
        np.delete(self.element, -1)  # del the last element
        self.shiftdown(ind)

        return extraction











class Heapnodes:
    def __init__(self, size=10):
        self.elements = arr.Custom_Arr(size)
        self.size = size

    def addnode(self, vertex):  # here vertex must be Vertex obj
        self.elements.add(vertex)
        self.size = self.elements.size
        self.shiftup(self.size - 1)
        # the last, i.e. added vertex finds its right place

    def shiftup(self, ind):
        # if nodes in V-X updated their scores, use shift up
        if ind != 0:  # if not at top
            par = (ind - 1) // 2
            if self.elements[par].score > self.elements[ind].score:
            # score is an attr of Vertex, indicate the greed score
                self.elements[par], self.elements[ind] = self.elements[ind], self.elements[par]  # swap
                self.shiftup(par)  # recurse to grandparents

    def shiftdown(self, ind):
        if ind != self.size:  # i.e., not the last one
            i = ind
            son1 = i * 2 + 1
            son2 = i * 2 + 2
            if self.elements[ind].score < self.elements[son1].score:
                self.elements[son1], self.elements[ind] = self.elements[ind], self.elements[son1]
                i = son1
            elif self.elements[ind].score < self.elements[son2].score:
                self.elements[son2], self.elements[ind] = self.elements[ind], self.elements[son2]
                i = son2
            else:
                break
            return shiftdown(self, i)

    def extract(self, ind=0):
        # use for push out the min root (ind=0) and update some elements
        extraction = self.elements[ind]
        self.elements[ind] = self.elements[-1]
        # move the last one to the extract place and shiftdown
        np.delete(self.element, -1)  # del the last element
        self.shiftdown(ind)

        return extraction  # return the extracted node

    def update(self, ind):  # ind is the extracted node id
        # use for update some nodes with score changed
        if self.elements[ind] < self.elements[(ind - 1) // 2]:
            self.shiftup(ind)
        elif self.elements[ind] > self.elements[ind * 2 + 1] or self.elements[ind] > self.elements[ind * 2 + 2]:
            self.shiftdown(ind)


    # def set_source(graph, ind):
    #     ind = ind - 1
    #     graph.nodes[ind].greedy = 0
    #     for i in range(0,len(graph.nodes[ind].connection)):
    #         graph.nodes[ind].connection[i].greedy = graph.nodes[ind].greedy + graph.nodes[ind].edgelen[i]
    # checklist = 
        
