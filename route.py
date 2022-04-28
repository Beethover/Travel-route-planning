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

# 单目的地
def weight(e, key):
    if key == 'TIME':
        return e.time
    if key == 'COST':
        return e.cost
    if key == 'CHANGE':
        return 1

def single_route(graph, start_vi, end_vi, key):
    # 分支界限法
    # 优先队列元素：（权值，出发点，到达点）
    viewQ = PrioQ()
    viewQ.enqueue((0, start_vi, start_vi))
    # route[i] 表示vi的前缀
    vnum = graph.get_vertex_num()
    route = [-1]*(vnum)
    route[start_vi] = start_vi
    # mini[i] 表示到vi的最小权值
    mini = [-1]*(vnum)
    mini[start_vi] = 0
    
    # 主循环
    f = False
    while not is_empty(viewQ):
        w, i, j = viewQ.dequeue()
        # 最优性剪枝
        if mini[j] >= 0 and w > mini[j]:
            # 不是最优
            continue
        route[j] = i
        mini[j] = w
        # 找到终点
        if j == end_vi:
            f = True
            break
        for e in graph.get_out_edges(j):
            viewQ.enqueue((w + weight(e,key), e.start.index, e.end.index))
        
    # 没找到
    if not f:
        raise ValueError('in route')
        
    # 返回路径（id）和权值
    p = end_vi
    road = [p]
    while p != start_vi:
        road.append(route[p])
    road.reverse()
    
    return road, w


# 多目的地
