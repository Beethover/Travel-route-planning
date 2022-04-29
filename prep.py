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
            if line == 'None\n':
                graph.vertices.append([None,None])
                continue
            index, name, belg, *tag = line[3:].split()
            v = View(name, belg, int(index), tag)
            graph.add_vertex(v)
            
    with open('routes.txt') as f:
        for line in f.readlines():
            if line == 'None\n':
                continue
            vi,_,ui,time,cost = line.split()
            vi = int(vi[3:]) ; ui = int(ui[3:])
            time = float(time)
            cost = float(cost)
            graph.add_edge(vi, ui, time, cost)

