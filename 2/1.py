import time
import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.patches as patches
import math as m

xfunc = lambda x, y: x*x-y*y+a
yfunc = lambda x, y: 2*x*y+b

xposition = lambda cell, leng: x0+h*(cell-(cell-1)//leng*leng-1)
yposition = lambda cell, leng: y1-h*((cell-1)//leng+1)

def cell_dribling(item, leng):
    lengnew = leng*2
    new1 = 2*item-1+(item-1)//leng*lengnew
    new2 = new1+1
    new3 = new1+lengnew
    new4 = new2+lengnew
    return [new1, new2, new3, new4]

def hyperloop(xdown, xup, ydown, yup, h, leng, G, s_list, pt):
    cou = 1
    xtmp = xdown
    ytmp = yup
    xckl = xdown
    yckl = yup
    cell_list = []
    while yckl > ydown:
        while xckl < xup:
            for i in range(0, pt):
                for j in range(0, pt):
                    xrz = xfunc(xtmp, ytmp)
                    yrz = yfunc(xtmp, ytmp)
                    xtmp += 1 / pt*h
                    # случай вылета за рамки
                    if xrz < xdown or xrz > xup or yrz < ydown or yrz > yup:
                        continue
                    cell = m.floor(((yup - yrz) / h)) * leng + m.ceil((xrz - xdown) / h) // 1 + 1
                    # для оптимизации
                    if cell_list != [] and cell_list.count(cell) != 0 or not(cell in s_list):
                        continue
                    elif yrz == ydown:  # случай попадения на нижнюю строку
                        if not ((cell - leng) in cell_list):
                            cell_list.append(cell - leng)
                    elif xrz == xdown:  # попал на левую границу
                        if not ((cell+1) in cell_list):
                            cell_list.append(cell+1)
                    elif not (cell in cell_list):   # default
                        cell_list.append(cell)
                xtmp = xckl
                ytmp -= 1 / pt*h
            xckl += h
            xtmp = xckl
            ytmp = yckl
            # print(cou,": ",cell_list)
            for i in range(0, len(cell_list)):
                G.add_edge(cou, cell_list[i])
            cou += 1
            cell_list.clear()
        yckl -= h
        xckl = xdown
        xtmp = xckl
        ytmp = yckl
    return G

x0 = -1.5
x1 = 1.5
y0 = -1.5
y1 = 1.5
h = 0.5
a = 0.3
b = 0.2

iterc = 6
pointcounter = 8
strxfunc = "x*x-y*y+a"
stryfunc = "2*x*y+b"
symbols = ["x","y","a","b"]

strxfunc = strxfunc.replace(symbols[2], a)
strxfunc = strxfunc.replace(symbols[3], b)
stryfunc = stryfunc.replace(symbols[2], a)
stryfunc = stryfunc.replace(symbols[3], b)

start_time = time.time()

lengx = abs(x1 - x0) / h
lengy = abs(y1 - y0) / h
list_good_dots = [q for q in range(1, int(lengx*lengy))]
G = nx.DiGraph()

for gh in range(1, (iterc+1)):
    
    G = hyperloop(x0, x1, y0, y1, h, lengx, G, list_good_dots, pointcounter)
    list_good_dots = list(G.nodes())  # номера ячеек, которые попали
    
    plt.figure(gh)
    plt.title(str(gh)+" iteration")
    plt.xlim((x0-1), (x1+1))
    plt.ylim((y0-1), (y1+1))
    plt.grid()
    ax = plt.gca()
    for c in nx.strongly_connected_components(G):
        if len(c) > 1:
            alist = list(c)
            for k in range(0, len(alist)):
                ss = patches.Rectangle((xposition(alist[k], lengx), yposition(alist[k], lengx)), h, h, color = 'blue', fill=True)
                ax.add_patch(ss)

    G.clear()
    newbuf = list_good_dots
    list_good_dots = []
    for i in range(0, len(newbuf)):
        r1 = cell_dribling(newbuf[i], lengx)
        list_good_dots += r1
    
    h *= 0.5
    lengx *= 2
    pointcounter -= 1
    print(gh, " iteration is done! Time elapsed: ", (time.time() - start_time))

plt.show()
