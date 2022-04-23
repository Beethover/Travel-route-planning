# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 15:22:23 2022

@author: DELL
"""

# 信息管理 用图存储

# 景点
class View():
    def __init__(self,name,belg,index,tag=None):
        # 名称，归属地，标签（用列表）
        self.name = name
        self.belong = belg
        self.index = index
        self.tag = []
        if tag is not None:
            self.tag = tag
        
        
    def add_tag(self,ad):
        # 用列表
        self.tag += ad
    
# 边结点
class ENode():
    def __init__(self,v,u,time,cost,nxt):
        # 边：起点，终点，耗时，花费
        self.start = v
        self.end = u
        self.time = time
        self.cost = cost
        self.next = nxt
        
    
# 路线
class Graph():
    def __init__(self):
        self.vertex_num = 0
        self.edges = []
        self.vertices = []
    
    def get_vertex_num(self):
        return self.vertex_num
    
    def add_vertex(self,v):
        # e.g. [v0,^]->[v1,t1,c1,^]->[v2,t2,c2,None]
        self.vertex_num += 1
        self.vertices.append([v,None])
    
    def add_edges(self,v,u,time,cost):
        # 采用邻接出边表
        edge = ENode(v,u,time,cost,None)
        self.edges.append(edge)
        p = self.vertices[v.index][1]
        if p is None:
            p = edge
        else:
            while p.next is not None:
                p = p.next
            p.next = edge
        
    def get_out_edges(self,vi):
        # 返回ENode组成的列表
        edges = []
        p = self.vertices[vi][1]
        while p is not None:
            edges.append(p)
            p = p.next
        return edges
    