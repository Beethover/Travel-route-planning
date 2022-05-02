# -*- coding: utf-8 -*-
"""
Created on Sat Apr 23 12:21:19 2022

@author: DELL
"""

# 路线规划
## 单一目的地 不同需求（时间、花费、少换乘等） 分支限界法
## 多目的地 AOV AOE

from infor import *
from prio_queue import PrioQ

def weight(e, key):
    if key == 'TIME':
        return (e.time,1,e.cost)
    if key == 'COST':
        return (e.cost,1,e.time)
    if key == 'CHANGE':
        return (1,e.time,e.cost)

def weight_sort(w, key):
    # time, cost, change
    if key == 'TIME':
        return (w[0], w[2], w[1])
    if key == 'COST':
        return (w[2], w[0], w[1])
    if key == 'CHANGE':
        return (w[1], w[2], w[0])

def nearest_route(graph, start_vi, dest, key):
    # 分支界限法
    # 优先队列元素：（权值，出发点，到达点）
    viewQ = PrioQ()
    viewQ.enqueue(( [0,0,0] , start_vi, start_vi))
    # route[i] 表示vi的前缀
    vnum = graph.get_vertex_num()
    route = [-1]*(vnum)
    route[start_vi] = start_vi
    # mini[i] 表示到vi的最小权值
    mini = [-1]*(vnum)
    mini[start_vi] = 0
    
    # 主循环
    f = False
    while not viewQ.is_empty():
        w, i, j = viewQ.dequeue()
        # 最优性剪枝
        if mini[j] >= 0 and w[0] > mini[j]:
            # 不是最优
            continue
        route[j] = i
        mini[j] = w
        # 找到终点
        if j in dest:
            f = True
            end_vi = j
            break
        for e in graph.get_out_edges(j):
            viewQ.enqueue(( [w[i] + weight(e,key)[i] for i in range(3)],\
                           e.start, e.end))
        
    # 没找到
    if not f:
        return False
        
    # 返回路径（id）和权值
    p = end_vi
    road = [p]
    while p != start_vi:
        road.append(route[p])
        p = route[p]
    road.reverse()
    
    return road, weight_sort(w, key)

# 单目的地
def single_route(graph, start_vi, end_vi, key):
    return nearest_route(graph, start_vi, [end_vi], key=key)

# 多目的地
# 遵循临近点原则，采用（权值，前驱）记录
def multi_route(graph, start_vi, dest):
    roads = [] ; wt = (0,0,0)
    dest_t = dest.copy()
    while dest_t:
        p = nearest_route(graph, start_vi, dest_t, key='CHANGE')
        if not p:
            return False
        road, w = p
        roads += road
        wt = [wt[i] + w[i] for i in range(3)]
        dest_t.remove(road[-1])
    return roads, wt
        
