# -*- coding: utf-8 -*-
"""
Created on Sat Apr 23 12:19:32 2022

@author: DELL
"""

import re

# 搜索景点
def search_v(name,graph):
    if name == '':
        return [i for i in range(len(graph.vertices)) \
                if graph.get_vertex_byid(i)!=None]
    suggestions = []
    p = '.*?'.join(name)
    rp = re.compile(p)
    for v,_ in graph.vertices:
        if v==None:
            continue
        match = rp.search(v.name)
        if match:
            suggestions.append([len(match.group()),match.start(),v.index])
    return [x for _,_,x in sorted(suggestions)]

# 搜索路线
def search_e(vi,ui,graph):
    p = graph.vertices[vi][1]
    while p is not None:
        if p.end == ui:
            return p
        p = p.next
    return False
