# -*- coding: utf-8 -*-
"""
Created on Sat Apr 23 14:03:36 2022

@author: DELL
"""

# 优先队列
class PrioQ():
    def __init__(self):
        self.elems = []
        self.size = 0
    
    def is_empty(self):
        return self.size == 0
    
    def enqueue(self,elem):
        self.size += 1
        self.elems.append(None)
        self.siftup(elem, self.size - 1)
        
    def siftup(self, elem, last):
        elems, i, j = self.elems, last, (last-1)//2
        while i>0 and elem < elems[j]:
            elems[i] = elems[j]
            i, j = j, (j-1)//2
        elems[i] = elem
    
    def dequeue(self):
        if self.is_empty():
            raise ValueError('in dequeue')
        self.size -= 1
        elems = self.elems
        e0 = elems[0]
        e = elems.pop()
        if len(elems):
            self.siftdown(e,0,len(elems))
        return e0
    
    def siftdown(self, elem, begin, end):
        elems, i, j, = self._elems, begin, begin*2+1
        while j<end:
            if j+1 < end and elems[j+1] < elems[j]:
                # j less than its brother
                j += 1
            if elem < elems[j]:
                break
            elems[i] = elems[j]
            i, j = j, 2*j+1
        elems[i] = elem
        
    
