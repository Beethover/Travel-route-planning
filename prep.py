# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 21:45:09 2022

@author: DELL
"""

# 数据预处理
# 从预存文件里爬数据
from infor import *
# 景点存储：序号(0起) 名称 归属地 标签
# 路线存储：起点序号 终点序号 耗时 花费
def read_in(graph):
    with open('views.txt') as f:
        for line in f.readlines():
            index, name, belg, *tag = line.split()
            v = View(name, belg, int(index), tag)
            graph.add_vertex(v)
            
    with open('routes.txt') as f:
        for line in f.readlines():
            vi,ui,time,cost = [float(x) for x in line.split()]
            v = graph.get_vertex_byid(int(vi))
            u = graph.get_vertex_byid(int(ui))
            graph.add_edge(v, u, time, cost)

