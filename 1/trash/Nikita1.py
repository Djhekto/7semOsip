from PySide6.QtWidgets import QApplication,QVBoxLayout, QGroupBox, QMainWindow, QVBoxLayout, QPushButton, QWidget, QStackedLayout,QLineEdit, QGridLayout, QLabel,QTableWidget, QTableWidgetItem
from PySide6.QtGui import QAction, QColor
from PySide6.QtCore import QSize
import numpy as np
import pyqtgraph as pg
from numpy import linalg as LA
from sympy import Symbol, diff, expand, Matrix

import numpy as np
from matplotlib import pyplot as plt
import sympy as sp
import math as ms
from scipy.spatial import distance

def start():

    x = sp.Symbol('x')
    y = sp.Symbol('y')
    a = sp.Symbol('a')
    a = 1.35
    h = 0.1

    X=eval("x + y + a*x*(1-x)")
    Y=eval("y + a*x*(1-x)")

    V1 = [eval( " ( (11**0.5)+1)/2 " ), eval( " 1 " )]
    V2 = [eval(" ( (11**0.5)-1)/2 "),  eval("-1")]


    def length(a, b):
        [x1, y1], [x2, y2] = a, b
        return (((x1-x2)**2)+((y1-y2)**2))**0.5

    def gen(a, b):
        x1 = X.subs({x: a[0], y: a[1]})
        y1 = Y.subs({x: a[0], y: a[1]})
        x2 = X.subs({x: b[0], y: b[1]})
        y2 = Y.subs({x: b[0], y: b[1]})

        if length([x1, y1], [x2, y2]) > h:
            return gen(a, [(a[0]+b[0])/2, (a[1]+b[1])/2])+gen([(a[0]+b[0])/2, (a[1]+b[1])/2], b)
        else:
            return [X.subs({x: a[0], y: a[1]}), Y.subs({x: a[0], y: a[1]})]

    def ccw(A,B,C):
        [ax, ay] = A
        [bx, by] = B
        [cx, cy] = C
        return (cy-ay)*(bx-ax) > (by-ay)*(cx-ax)
    
    def intersect(A,B,C,D):
            return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

    def coef(a, b):
        (x1, y1) = a[0]
        (x2, y2) = a[1]
        (X1, Y1) = b[0]
        (X2, Y2) = b[1]
        if intersect(a[0], a[1], b[0], b[1]) == True:
            a1, b1, c1 = 1/(x2-x1), -1/(y2-y1), x1/(x2-x1) - y1/(y2-y1)
            a2, b2, c2 = 1/(X2-X1), -1/(Y2-Y1), X1/(X2-X1) - Y1/(Y2-Y1)
            if (a1*b2-a2*b1) != 0:
                ha = [(c1*b2-c2*b1)/(a1*b2-a2*b1), (a1*c2-a2*c1)/(a1*b2-a2*b1)]
                if (ha[0] == 0) and (ha[1] == 0):
                    return 0
                else:
                    if (min(x1, x2) <= ha[0]) and (max(x1, x2) >= ha[0]):
                        if (min(X1, X2) <= ha[0]) and (max(X1, X2) >= ha[0]):
                            if (min(y1, y2) <= ha[1]) and (max(y1, y2) >= ha[1]):
                                if (min(Y1, Y2) <= ha[1]) and (max(Y1, Y2) >= ha[1]):
                                    return ha
            else:
                return 0
        else: 
            return 0

    V1_x_folder = [0.0, V1[0], X.subs({x: V1[0], y: V1[1]})]
    V1_y_folder = [0.0, V1[1], Y.subs({x: V1[0], y: V1[1]})]
    
    for i in range(0):
        X_current =X.subs({x: V1_x_folder[-1], y: V1_y_folder[-1]})
        Y_current = Y.subs({x: V1_x_folder[-1], y: V1_y_folder[-1]})
        V1_x_folder.append(X_current)
        V1_y_folder.append(Y_current)
    
    print(V1_x_folder)
    print(V1_y_folder)

    u = []
    for i in range(len(V1_x_folder)-1):
        u = u + gen([V1_x_folder[i], V1_y_folder[i]], [V1_x_folder[i+1], V1_y_folder[i+1]])
    #print(u)
    V1_x_folder, V1_y_folder = u[0::2], u[1::2]

    X=eval("x - y")
    Y=eval("y - a*(x-y)*(1-x+y)" )

    V2_x_folder = [0.0, V2[0], X.subs({x: V2[0], y: V2[1]})]
    V2_y_folder = [0.0, V2[1], Y.subs({x: V2[0], y: V2[1]})]

    for i in range(0):
        X_current =X.subs({x: V2_x_folder[-1], y: V2_y_folder[-1]})
        Y_current = Y.subs({x: V2_x_folder[-1], y: V2_y_folder[-1]})
        V2_x_folder.append(X_current)
        V2_y_folder.append(Y_current)
        
    print(V2_x_folder)
    print(V2_y_folder)
    
    u = []
    for i in range(len(V2_x_folder)-1):
        u = u + gen([V2_x_folder[i], V2_y_folder[i]], [V2_x_folder[i+1], V2_y_folder[i+1]])
    print(u)
    V2_x_folder, V2_y_folder = u[0::2], u[1::2]
    
    def intersection(V1_x_folder, V1_y_folder, V2_x_folder, V2_y_folder):
        first_list = list(zip(V1_x_folder,V1_y_folder))
        second_list = list(zip(V2_x_folder, V2_y_folder))
        for i in range(len(first_list)-1):
            for j in range(len(second_list)-1):
                saver = coef([first_list[i], first_list[i+1]], [second_list[j], second_list[j+1]])
                if saver != 0 and saver != None:                
                    V1_x_folder = V1_x_folder[:i+1] 
                    V1_x_folder.append(saver[0])
                    V2_x_folder = V2_x_folder[:j+1] 
                    V2_x_folder.append(saver[0])
                    V1_y_folder = V1_y_folder[:i+1] 
                    V1_y_folder.append(saver[1])
                    V2_y_folder = V2_y_folder[:j+1] 
                    V2_y_folder.append(saver[1])
                    return [[V1_x_folder, V1_y_folder], [V2_x_folder, V2_y_folder]]
    
    u = intersection(V1_x_folder, V1_y_folder, V2_x_folder, V2_y_folder)


start()

