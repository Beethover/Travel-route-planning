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
    tp.geometry('250x50')
    Label(tp, text = text).pack()

def search_view_window(key):
    global svw, e1, c2, c3
    # 查询
    svw = Toplevel()
    svw.title('查询景点')
    
    Label(svw, text = '景点名称：').grid(row=0, column=0)
    v1 = StringVar()
    e1 = Entry(svw, textvariable=v1)
    e1.grid(row=0, column=1,padx=10,pady=5)
    
    Label(svw, text = '景点归属地：').grid(row=1, column=0)
    v2 = StringVar()
    c2 = ttk.Combobox(svw, textvariable=v2)
    c2.grid(row=1, column=1,padx=10,pady=5)
    c2['values'] = ['None'] + list(graph.belongs)
    c2.current(0)
    
    Label(svw, text = '景点标签：').grid(row=2, column=0)
    v3 = StringVar()
    c3 = ttk.Combobox(svw, textvariable=v3)
    c3.grid(row=2, column=1,padx=10,pady=5)
    c3['values'] = ['None'] + list(graph.tags)
    c3.current(0)
    
    Button(svw, text = '查询', command = lambda:search_return(key))\
        .grid(row=3, column=1, sticky=W, padx=10, pady=5)

def search_return(key):
    global sr
    name = e1.get()
    suggestions = search_v(name, graph)
    belg = c2.get()
    tag = c3.get()
    for i in reversed(suggestions):
        v = graph.get_vertex_byid(i)
        if (belg != '' and belg != v.belong)\
            or (tag != '' and tag not in v.tag):
                suggestions.remove(i)
    sr = Toplevel()
    sr.title('查找结果')
    sr.geometry('400x200')
    lb = Listbox(sr, selectmode = EXTENDED)
    lb.pack(side=LEFT, fill=BOTH, expand=True)
    if suggestions:
        for vi in suggestions:
            lb.insert(END, graph.get_vertex_byid(vi))
    else:
        sr.destroy()
        Tp('错误发生！','无结果！')
        
    if key == 'CHECK':
        return
    if key == 'DELETE':
        text = '删除'
        cmd = lambda x=lb: delete_view_tp(suggestions[x.curselection()[0]])
    if key == 'CHANGE':
        text = '修改'
        cmd = lambda x=lb: \
            change_view_window(suggestions[x.curselection()[0]])
    if key[:-1] == 'CHOOSE_':
        text = '选择'
        cmd = lambda x=lb: v_get(key[-1], suggestions[x.curselection()[0]])
    
    Button(sr, text = text, command = cmd)\
        .pack(padx=10, pady=5)
    
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
    
    # 改文件
    with open('views.txt','a') as f:
        f.write('NO.%d %s %s '%(index,name,belg) + ' '.join(tag) + '\n')
    
    add.destroy()

def delete_view_tp(vi):
    graph.del_vertex(vi)
    Tp('好耶！','删除成功！')
    
    # 改文件
    with open('views.txt','r') as f:
        content = f.read()
        pos1 = content.find('NO.%d '%vi)
        pos2 = content.find('\n', pos1+1)
        content = content[:pos1] + 'None' + '\n' + \
            content[pos2+1:]
    with open('views.txt','w') as f:
        f.write(content)
    
    
    sr.destroy()
    
def change_view_window(vi):
    global cvw,e1,e2,e3
    old_name = graph.get_vertex_byid(vi).name
    old_belg = graph.get_vertex_byid(vi).belong
    old_tag = graph.get_vertex_byid(vi).tag
    
    cvw = Toplevel()
    cvw.title('修改景点')
    
    Label(cvw, text = '景点名称：').grid(row=0, column=0)
    v1 = StringVar()
    v1.set(old_name)
    e1 = Entry(cvw, textvariable=v1)
    e1.grid(row=0, column=1,padx=10,pady=5)
    
    Label(cvw, text = '景点归属地：').grid(row=1, column=0)
    v2 = StringVar()
    v2.set(old_belg)
    e2 = Entry(cvw, textvariable=v2)
    e2.grid(row=1, column=1,padx=10,pady=5)
    
    Label(cvw, text = '景点标签：').grid(row=2, column=0)
    v3 = StringVar()
    v3.set(old_tag)
    e3 = Entry(cvw, textvariable=v3)
    e3.grid(row=2, column=1,padx=10,pady=5)

    Button(cvw, text = '修改', command = lambda:change_v(vi))\
    .grid(row=3, column=1, sticky=W, padx=10, pady=5)
    
def change_v(vi):
    name = e1.get()
    belg = e2.get()
    tag = e3.get().split()
    
    new_v = View(name, belg, vi, tag)
    graph.change_vertex(new_v)
    
    Tp('好耶！','修改成功！')
    #改文件
    with open('views.txt','r') as f:
        content = f.read()
        pos1 = content.find('NO.%d '%vi)
        pos2 = content.find('\n', pos1+1)
        content = content[:pos1] + \
            'NO.%d %s %s '%(vi,name,belg) + ' '.join(tag) + '\n' + \
            content[pos2+1:]
    with open('views.txt','w') as f:
        f.write(content)
    
    sr.destroy()
    cvw.destroy()

def v_get(p, get):
    global vi, ui, start_vi, end_ui
    if p=='1':
        vi = get
        t1.set(graph.get_vertex_byid(vi))
    if p=='2':
        ui = get
        t2.set(graph.get_vertex_byid(ui))
    if p=='i':
        start_vi = get
        start_inf.set(graph.get_vertex_byid(start_vi))
    if p=='d':
        end_ui = get
        txt.set(graph.get_vertex_byid(end_ui))
    if p=='m':
        dest.append(get)
        mlb.insert(END, graph.get_vertex_byid(get))
    sr.destroy()
    svw.destroy()
    
def add_edge_window():
    # 增加路线
    global add,vi,ui,t1,t2,e3,e4
    add = Toplevel()
    add.title('增加路线')
    
    vi = -1; ui = -1
    
    Label(add, text = '起点：').grid(row=0, column=0)
    t1 = StringVar()
    t1.set('请选择')
    Label(add, textvariable = t1).grid(row=0,column=1)
    Button(add, text = '选择', \
           command=lambda:search_view_window('CHOOSE_1'))\
        .grid(row=0, column=2)
        
    Label(add, text = '终点：').grid(row=1, column=0)
    t2 = StringVar()
    t2.set('请选择')
    Label(add, textvariable = t2).grid(row=1,column=1)
    Button(add, text = '选择', \
           command=lambda:search_view_window('CHOOSE_2'))\
        .grid(row=1, column=2)
    
    Label(add, text = '耗时：').grid(row=2,column=0)
    v3 = StringVar()
    e3 = Entry(add, textvariable = v3)
    e3.grid(row=2,column=1)
    
    Label(add, text = '花费：').grid(row=3,column=0)
    v4 = StringVar()
    e4 = Entry(add, textvariable = v4)
    e4.grid(row=3,column=1)
    
    Button(add, text = '增加', command = get_newe).\
        grid(row=4, column=1, padx=10, pady=5)
        
def get_newe():
    try:
        time = float(e3.get())
        cost = float(e4.get())    
        
        graph.add_edge(vi, ui, time, cost)
        
        Tp('好耶！','增加成功！')
        
        # 改文件
        with open('routes.txt','a') as f:
            f.write('NO.%d to NO.%d %8.2f %8.2f '%(vi,ui,time,cost) + '\n')
        
        add.destroy()
    except:
        Tp('错误发生！','请输入正确的数据！')

def search_edge_window(key):
    global sew, vi, ui, t1, t2
    sew = Toplevel()
    sew.title('查找路线')
    
    vi = -1; ui = -1
    
    Label(sew, text = '起点：').grid(row=0, column=0)
    t1 = StringVar()
    t1.set('请选择')
    Label(sew, textvariable = t1).grid(row=0,column=1)
    Button(sew, text = '选择', \
           command=lambda:search_view_window('CHOOSE_1'))\
        .grid(row=0, column=2)
        
    Label(sew, text = '终点：').grid(row=1, column=0)
    t2 = StringVar()
    t2.set('请选择')
    Label(sew, textvariable = t2).grid(row=1,column=1)
    Button(sew, text = '选择', \
           command=lambda:search_view_window('CHOOSE_2'))\
        .grid(row=1, column=2)
    
    Button(sew, text = '搜索', command = lambda: search_edge_return(key))\
        .grid(row=2, column=1)

def search_edge_return(key):
    global sr
    edge = search_e(vi, ui, graph)
    if edge:
        sr = Toplevel()
        sr.title('路线信息')
        sr.geometry('300x50')
        
        edge_inf = '耗时：%-3d时%-3d分  花费：%-8.2f元'%\
            (int(edge.time//60), int(edge.time%60), edge.cost)
        Label(sr, text = edge_inf).pack()
        
        if key == 'CHECK':
            return
        if key == 'DELETE':
            text = '删除'
            cmd = lambda: delete_edge_tp(edge)
        if key == 'CHANGE':
            text = '修改'
            cmd = lambda: change_edge_window(edge)
        
        
        Button(sr, text = text, command = cmd).pack()
        
    else:
        Tp('错误发生！','不存在这条路线！')
        
def delete_edge_tp(edge):
    graph.del_edge(edge)
    Tp('好耶！','删除成功！')
    
    # 改文件
    with open('routes.txt','r') as f:
        content = f.read()
        pos1 = content.find('NO.%d to NO.%d'%(edge.start, edge.end))
        pos2 = content.find('\n', pos1+1)
        content = content[:pos1] + 'None' + '\n' + \
            content[pos2+1:]
    with open('routes.txt','w') as f:
        f.write(content)
    
    sr.destroy()

def change_edge_window(edge):
    global cew, e1, e2
    
    old_time = edge.time
    old_cost = edge.cost
    
    cew = Toplevel()
    cew.title('修改路线')
    
    Label(cew, text = '耗时：').grid(row=0,column=0)
    v1 = StringVar()
    v1.set(old_time)
    e1 = Entry(cew, textvariable = v1)
    e1.grid(row=0,column=1)
    
    Label(cew, text = '花费：').grid(row=1,column=0)
    v2 = StringVar()
    v2.set(old_cost)
    e2 = Entry(cew, textvariable = v2)
    e2.grid(row=1,column=1)
    
    Button(cew, text = '修改', command = lambda:change_e(edge)).\
        grid(row=2, column=1,sticky=W, padx=10, pady=5)

def change_e(edge):
    vi = edge.start ; ui = edge.end
    time = float(e1.get())
    cost = float(e2.get())
    
    graph.del_edge(edge)
    graph.add_edge(vi, ui, time, cost)
    
    Tp('好耶！','修改成功！')
    
    # 改文件
    with open('routes.txt','r') as f:
        content = f.read()
        pos1 = content.find('NO.%d to NO.%d'%(edge.start, edge.end))
        pos2 = content.find('\n', pos1+1)
        content = content[:pos1] + \
            'NO.%d to NO.%d %8.2f %8.2f '%(vi,ui,time,cost) + '\n' + \
            content[pos2+1:]
    with open('routes.txt','w') as f:
        f.write(content)
    
    sr.destroy()
    cew.destroy()

def single_route_window():
    global srw, end_ui, txt, iv
    if start_vi == -1:
        Tp('错误发生！','请先完善起点信息！')
        return
    srw = Toplevel()
    srw.title('单目的地规划')
    
    Label(srw, text = '目的地：').grid(row = 0, column = 0)
    
    end_ui = -1
    txt = StringVar()
    txt.set('请选择')
    Label(srw, textvariable=txt).grid(row = 0, column = 1)
    
    Button(srw, text = '选择', \
           command=lambda:search_view_window('CHOOSE_d'))\
        .grid(row = 0, column = 2)
        
    group = LabelFrame(srw, text = '规划倾向')
    group.grid(row = 1, column = 1)
    iv = IntVar()
    iv.set(0)
    KEY = [
        ('时间最少',0),
        ('花钱最少',1),
        ('换乘最少',2)]
    for k,num in KEY:
        Radiobutton(group,
                text=k,
                variable=iv,
                value=num,
                indicatoron=False).pack(anchor=W, padx = 10, pady = 5)

    
    Button(srw, text = '开始规划', \
           command=single_route_return)\
        .grid(row = 2, column = 1, pady = 10)

def single_route_return():
    key = ['TIME','COST','CHANGE'][iv.get()]
    p = single_route(graph, start_vi, end_ui, key)
    if not p:
        Tp('错误发生！','找不到去这里的路！')
        return
    route_return(p, end_ui)
    
def route_return(p, *dest):
    road,w = p
    srr = Toplevel()
    srr.title('规划结果')
    srr.geometry('300x200')
    
    Label(srr, text = '从 %s 出发'%graph.get_vertex_byid(start_vi).name)\
        .pack()
    
    for i in road[1:]:
        if i in dest:
            Label(srr, text = '到达目的地：%s'%\
                  graph.get_vertex_byid(i).name)\
                .pack()
        else:
            Label(srr, text = '经过：%s'%graph.get_vertex_byid(i).name)\
                .pack()
    
   
    Label(srr, text = '总共耗时%-3d时%-3d分\n花费%-8.2f元\n换乘%d次'%\
          (int(w[0]//60), int(w[0]%60), w[1], w[2])).pack()
    
def multi_route_window():
    global dest, mlb
    if start_vi == -1:
        Tp('错误发生！','请先完善起点信息！')
        return

    mrw = Toplevel()
    mrw.title('多目的地规划')
    mrw.geometry('500x200')
    
    lframe = Frame(mrw)
    rframe = Frame(mrw)
    
    dest = []
    mlb = Listbox(lframe, selectmode=EXTENDED)
    mlb.pack(side=LEFT, fill=BOTH, expand=True)
    
    Button(rframe, text = '增加目的地', \
           command = lambda:search_view_window('CHOOSE_m'))\
        .grid(row=0, padx = 5, pady = 10)
    Button(rframe, text = '删除目的地', \
           command = delete_dest)\
        .grid(row=1, padx = 5, pady = 10)
    Button(rframe, text = '开始规划', \
           command = multi_route_return)\
        .grid(row=2, padx = 5, pady = 10)
    
    lframe.pack(side=LEFT, fill=BOTH, expand=True)
    rframe.pack(side=RIGHT)

def delete_dest():
    get = dest[mlb.curselection()[0]]
    dest.remove(get)
    mlb.delete(ACTIVE)

def multi_route_return():
    p = multi_route(graph, start_vi, dest)
    if not p:
        Tp('错误发生！','找不到去这里的路！')
        return
    route_return(p, dest)

# 页面设计 Tkinter
def main():
    global start_inf, start_vi
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
    view_mng.add_command(label = '修改', \
                         command=lambda:search_view_window('CHANGE'))
    menubar.add_cascade(label = '景点管理', menu = view_mng)
    
    # 路线管理 - 增加 - 删除 - 修改
    edge_mng = Menu(menubar, tearoff = False)
    edge_mng.add_command(label = '增加', command = add_edge_window)
    edge_mng.add_separator()
    edge_mng.add_command(label = '删除', \
                         command = lambda:search_edge_window('DELETE'))
    edge_mng.add_command(label = '修改', \
                         command = lambda:search_edge_window('CHANGE'))
    menubar.add_cascade(label = '路线管理', menu = edge_mng)
    
    
    # 页面
    # 按钮功能
    Bframe = Frame(root)
    ## 查询
    Button(Bframe, text = '查询景点', \
           command=lambda:search_view_window('CHECK'))\
        .grid(row = 0, column = 0, padx = 10, pady = 20)
    Button(Bframe, text = '查询路线', \
           command=lambda:search_edge_window('CHECK'))\
        .grid(row = 0, column = 1, padx = 10, pady = 20)
    
    ## 路线规划
    Button(Bframe, text = '单目的地规划', \
           command = single_route_window)\
        .grid(row = 1, column = 0, padx = 10)
    Button(Bframe, text = '多目的地规划', \
           command = multi_route_window)\
        .grid(row = 1, column = 1, padx = 10)
    
    Bframe.pack(side=TOP)
    
    # 显示器
    Lframe = Frame(root)
    # 完善起点信息
    Button(Lframe, text = '完善起点信息', \
           command=lambda:search_view_window('CHOOSE_i'))\
        .pack()
    start_vi = -1
    start_inf = StringVar()
    start_inf.set('请先完善起点信息！')
    Label(Lframe, textvariable=start_inf).pack(pady = 20)
    
    
    Lframe.pack(side=TOP, pady = 50)
    
    root.config(menu = menubar)
    
    root.mainloop()

if __name__ == '__main__':
    main()