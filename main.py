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
from tkinter import ttk
from prep import *

graph = Graph()
read_in(graph)


# 页面函数
def Tp(title, text):
    tp = Toplevel()
    tp.title(title)
    tp.geometry('200x50')
    Label(tp, text = text).pack()
    

def add_view_window():
    # 增加景点
    global add,e1,e2,e3
    add = Toplevel()
    add.title('增加景点')
    
    Label(add, text = '景点名称：').grid(row=0, column=0)
    v1 = StringVar()
    e1 = Entry(add, textvariable=v1)
    e1.grid(row=0, column=1,padx=10,pady=5)
    
    Label(add, text = '景点归属地：').grid(row=1, column=0)
    v2 = StringVar()
    e2 = Entry(add, textvariable=v2)
    e2.grid(row=1, column=1,padx=10,pady=5)
    
    Label(add, text = '景点标签：').grid(row=2, column=0)
    v3 = StringVar()
    e3 = Entry(add, textvariable=v3)
    e3.grid(row=2, column=1,padx=10,pady=5)


    Button(add, text = '增加', command = get_newv)\
    .grid(row=3, column=1, sticky=W, padx=10, pady=5)
    
def get_newv():
    name = e1.get()
    belg = e2.get()
    if name=='' or belg=='':
        Tp('错误发生！','请完成输入后再增加！')
        return
    
    tag = e3.get().split()
    index = graph.get_vertex_num()
    graph.add_vertex(View(name,belg,index,tag))
    
    Tp('好耶！','增加成功！')
    
    with open('views.txt','a') as f:
        f.write('%d %s %s '%(index,name,belg) + ' '.join(tag) + '\n')
    
    add.destroy()


def search_view_window(key):
    global svw, e1, c2, c3
    # 查询
    svw = Toplevel()
    svw.title('查询景点')
    
    Label(svw, text = '景点名称：').grid(row=0, column=0)
    Label(svw, text = '景点归属地：').grid(row=1, column=0)
    Label(svw, text = '景点标签：').grid(row=2, column=0)
    
    v1 = StringVar()
    e1 = Entry(svw, textvariable=v1)
    e1.grid(row=0, column=1,padx=10,pady=5)
    
    v2 = StringVar()
    c2 = ttk.Combobox(svw, textvariable=v2)
    c2.grid(row=1, column=1,padx=10,pady=5)
    c2['values'] = ['None'] + list(graph.belongs)
    c2.current(0)
    
    v3 = StringVar()
    c3 = ttk.Combobox(svw, textvariable=v3)
    c3.grid(row=2, column=1,padx=10,pady=5)
    c3['values'] = ['None'] + list(graph.tags)
    c3.current(0)
    
    Button(svw, text = '查询', command = lambda:search_return(key))\
        .grid(row=3, column=1, sticky=W, padx=10, pady=5)

def search_return(key):
    name = e1.get()
    suggestions = search_v(name, graph)
    belg = c2.get()
    tag = c3.get()
    for vi in suggestions:
        v = graph.get_vertex_byid(vi)
        if belg != '' and belg != v.belong\
            or tag != '' and tag not in v.tag:
                suggestions.remove(vi)
    
    tp = Toplevel()
    tp.title('查找结果')
    tp.geometry('400x200')
    lb = Listbox(tp, selectmode = EXTENDED)
    lb.pack(side=LEFT, fill=BOTH, expand=True)
    for vi in suggestions:
        lb.insert(END, graph.get_vertex_byid(vi))
        
    if key == 'CHECK':
        return
    if key == 'DELETE':
        text = '删除'
        cmd = lambda x=lb: graph.del_vertex(x.curselection()[0])
    
    Button(tp, text = text, command = cmd)\
        .pack(padx=10, pady=5)


# 页面设计 Tkinter
root = Tk()
root.title('旅游规划宝')
root.geometry('500x500')

# Menu
menubar = Menu(root)
# 景点管理 - 增加 - 删除 - 修改
    
view_mng = Menu(menubar, tearoff = False)
view_mng.add_command(label = '增加', command = add_view_window)
view_mng.add_separator()
view_mng.add_command(label = '删除', \
                     command=lambda:search_view_window('DELETE'))
view_mng.add_command(label = '修改')
menubar.add_cascade(label = '景点管理', menu = view_mng)

# 路线管理 - 增加 - 删除 - 修改
edge_mng = Menu(menubar, tearoff = False)
edge_mng.add_command(label = '增加')
edge_mng.add_separator()
edge_mng.add_command(label = '删除')
edge_mng.add_command(label = '修改')
menubar.add_cascade(label = '路线管理', menu = edge_mng)

Button(root, text = '查询景点', \
       command=lambda:search_view_window('CHECK'))\
    .pack(pady = 20)

root.config(menu = menubar)

root.mainloop()