# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 12:36:49 2022

@author: DELL
"""

# 旅游规划
# copyright 2100011461 物理学院 陈贝宁

# 信息管理：增删改(开发者模式)
## 景点信息：名称、归属地、标签等
## 路线信息：出发地、到达地、时间、花费等

# 信息查询
## 关键字查询 

# 路线规划
## 单一目的地 不同需求（时间、花费、少换乘等）
## 多目的地
from infor import *
from search import *
from route import *
from tkinter import *
from prep import *

graph = Graph()
read_in(graph)


# 页面设计 Tkinter
root = Tk()
root.title('旅游规划宝')

# Menu
menubar = Menu(root)
# 景点管理 - 增加 - 删除 - 修改
def add_view_window():
    # 增加景点
    global add,e11,e12,e13
    add = Toplevel()
    add.title('增加景点')
    
    Label(add, text = '景点名称：').grid(row=0, column=0)
    v11 = StringVar()
    e11 = Entry(add, textvariable=v11)
    e11.grid(row=0, column=1,padx=10,pady=5)
    
    Label(add, text = '景点归属地：').grid(row=1, column=0)
    v12 = StringVar()
    e12 = Entry(add, textvariable=v12)
    e12.grid(row=1, column=1,padx=10,pady=5)
    
    Label(add, text = '景点标签：').grid(row=2, column=0)
    v13 = StringVar()
    e13 = Entry(add, textvariable=v13)
    e13.grid(row=2, column=1,padx=10,pady=5)


    Button(add, text = '增加', command = get_newv)\
    .grid(row=3, column=1, sticky=W, padx=10, pady=5)
    
def get_newv():
    name = e11.get()
    belg = e12.get()
    tag = e13.get().split()
    index = graph.get_vertex_num()
    graph.add_vertex(View(name,belg,index,tag))
    
    tp = Toplevel()
    tp.title('好耶！')
    Label(tp, text = '增加成功！').pack()
    
    add.destroy()
    

view_mng = Menu(menubar, tearoff = False)
view_mng.add_command(label = '增加', command = add_view_window)
view_mng.add_separator()
view_mng.add_command(label = '删除')
view_mng.add_command(label = '修改')
menubar.add_cascade(label = '景点管理', menu = view_mng)
# 路线管理 - 增加 - 删除 - 修改
edge_mng = Menu(menubar, tearoff = False)
edge_mng.add_command(label = '增加')
edge_mng.add_separator()
edge_mng.add_command(label = '删除')
edge_mng.add_command(label = '修改')
menubar.add_cascade(label = '路线管理', menu = edge_mng)

# 查询
Label(root, text = '景点名称：').grid(row=0, column=0)
Label(root, text = '景点归属地：').grid(row=1, column=0)
Label(root, text = '景点标签：').grid(row=2, column=0)

v1 = StringVar()
e1 = Entry(root, textvariable=v1)
e1.grid(row=0, column=1,padx=10,pady=5)

v2 = StringVar()
e2 = Entry(root, textvariable=v2)
e2.grid(row=1, column=1,padx=10,pady=5)

v3 = StringVar()
e3 = Entry(root, textvariable=v3)
e3.grid(row=2, column=1,padx=10,pady=5)

Button(root, text = '查询')\
    .grid(row=3, column=1, sticky=W, padx=10, pady=5)


root.config(menu = menubar)

root.mainloop()