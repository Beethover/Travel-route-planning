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
        if tag is not None:
            self.tag = tag
        else:
            self.tag = []
        
        
    def add_tag(self,ad):
        # 用列表
        self.tag += ad
        
    def __str__(self):
        return '景点名称：%-8s归属地：%-8s标签：%s' \
            % (self.name, self.belong, self.tag)
    
# 边结点
class ENode():
    def __init__(self,vi,ui,time,cost,nxt):
        # 边：起点，终点，耗时（分钟），花费
        self.start = vi
        self.end = ui
        self.time = time
        self.cost = cost
        self.next = nxt
        
    
# 路线
class Graph():
    def __init__(self):
        self.vertex_num = 0
        self.edges = []
        self.vertices = []
        self.belongs = set() 
        self.tags = set()
    
    def get_vertex_num(self):
        return len(self.vertices)
    
    def add_vertex(self,v):
        # e.g. [v0,^]->[e1,^]->[e2,None]
        self.vertex_num += 1
        self.vertices.append([v,None])
        self.belongs.add(v.belong)
        for t in v.tag:
            self.tags.add(t)
        
    def change_vertex(self,new_v):
        index = new_v.index
        self.vertices[index][0] = new_v
        
    def get_vertex_byid(self,index):
        return self.vertices[index][0]
    
    def del_vertex(self,vi):
        self.vertices[vi] = [None, None]
        self.vertex_num -= 1
    
    def add_edge(self,vi,ui,time,cost):
        # 采用邻接出边表
        edge = ENode(vi,ui,time,cost,None)
        self.edges.append(edge)
        p = self.vertices[vi][1]
        if p is None:
            self.vertices[vi][1] = edge
        else:
            while p.next is not None:
                p = p.next
            p.next = edge
        
    def del_edge(self,edge):
        vi = edge.start
        p = self.vertices[vi][1]
        if p == edge:
            self.vertices[vi][1] = p.next
        else:
            while p.next is not None:
                if p.next == edge:
                    p.next = p.next.next
                else:
                    p = p.next                    
    
    def get_out_edges(self,vi):
        # 返回ENode组成的列表
        edges = []
        p = self.vertices[vi][1]
        while p is not None:
            edges.append(p)
            p = p.next
        return edges
    
    