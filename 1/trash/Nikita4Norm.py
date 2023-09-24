from PySide6.QtWidgets import QApplication,QVBoxLayout, QGroupBox, QMainWindow, QVBoxLayout, QPushButton, QWidget, QStackedLayout,QLineEdit, QGridLayout, QLabel,QTableWidget, QTableWidgetItem
from PySide6.QtGui import QAction, QColor
from PySide6.QtCore import QSize
import numpy as np
import pyqtgraph as pg
from numpy import linalg as LA
#from sympy import Symbol, diff, expand, Matrix

from math import log

import sympy as sp
import math as ms
from scipy.spatial import distance

class MainWindow(QMainWindow): 
    myiter = 0
    
    def __init__(self): 
        super(MainWindow, self).__init__()
        self.setWindowTitle("Homoclinical dot and smth else")
        self.layout_stack = QStackedLayout()

#--------------------------------------------------------------------------
        self.layout_input = QGridLayout()

        self.fun1 = QLineEdit( "x + y + a*x*(1-x)" )
        self.fun2 = QLineEdit( "y + a*x*(1-x)" )
        self.fun1rev = QLineEdit( "x - y" )
        self.fun2rev = QLineEdit( "a*(x**2) - a*x + a*(y**2) + a*y - 2*a*x*y + y" )
        self.parvalue = QLineEdit( "1.35" )
        self.parname = QLineEdit( "a" )
        self.accvalue = QLineEdit( "0.1" )
        self.symbols = QLineEdit( "x,y" )
        self.iterc = QLineEdit( "100" )
        self.iterp = QLineEdit( "10" )
        self.start = QLineEdit( "[0,0]")
        self.v1x = QLineEdit( " 2.1583123951777 ")
        self.v1y = QLineEdit( " 1 ")
        self.v2x = QLineEdit( " 1.1583123951777 ")
        self.v2y = QLineEdit( " -1 ")

        self.button1 = QPushButton("построить график")
        self.button1.clicked.connect(self.clearandplot)
        self.button3 = QPushButton("дополнить график")
        self.button3.clicked.connect(self.myplot )

        self.group1 = QGroupBox("Система уравнений")
        self.group1.setMaximumSize(QSize(300, 200)) 
        layout1 = QVBoxLayout()
        layout1.addWidget(self.fun1)
        layout1.addWidget(self.fun2)
        self.group1.setLayout(layout1)        
        self.layout_input.addWidget( self.group1 ,1 , 0)

        self.group1 = QGroupBox("Обратная система уравнений")
        self.group1.setMaximumSize(QSize(300, 200)) 
        layout1 = QVBoxLayout()
        layout1.addWidget(self.fun1rev)
        layout1.addWidget(self.fun2rev)
        self.group1.setLayout(layout1)        
        self.layout_input.addWidget( self.group1 ,1 ,1)
        
        self.group1 = QGroupBox("Значение и символ параметра")
        self.group1.setMaximumSize(QSize(300, 100)) 
        layout1 = QGridLayout()
        layout1.addWidget(self.parvalue , 0 , 0 )
        layout1.addWidget(self.parname , 0, 1)
        self.group1.setLayout(layout1)        
        self.layout_input.addWidget( self.group1 ,2 ,0)
        
        self.group1 = QGroupBox("Начальная точка и точность")
        self.group1.setMaximumSize(QSize(300, 100)) 
        layout1 = QGridLayout()
        layout1.addWidget(self.start , 0 , 0 )
        layout1.addWidget(self.accvalue , 0, 1)
        self.group1.setLayout(layout1)        
        self.layout_input.addWidget( self.group1 ,2 ,1 )

        self.group1 = QGroupBox("Кол-во итераций посчитать сразу и по кнопке")
        self.group1.setMaximumSize(QSize(300, 200)) 
        layout1 = QGridLayout()
        layout1.addWidget(self.iterc , 0 , 0 )
        layout1.addWidget(self.iterp , 0, 1)
        layout1.addWidget(self.button1 , 1 , 0 )
        layout1.addWidget(self.button3 , 1, 1)
        self.group1.setLayout(layout1)        
        self.layout_input.addWidget( self.group1 ,3 ,0 )

        self.group1 = QGroupBox("Значения собственных векторов")
        self.group1.setMaximumSize(QSize(300, 200)) 
        layout1 = QGridLayout()
        bsup1 = QLabel("вектор 1"); bsup1.setMaximumSize(QSize(200, 10))
        bsup2 = QLabel("вектор 2"); bsup2.setMaximumSize(QSize(200, 10))
        layout1.addWidget(bsup1 , 0 , 0 )
        layout1.addWidget(bsup2 , 0 , 1 )
        layout1.addWidget(self.v1x , 1 , 0 )
        layout1.addWidget(self.v1y , 2, 0)
        layout1.addWidget(self.v2x , 1 , 1 )
        layout1.addWidget(self.v2y , 2, 1)
        self.group1.setLayout(layout1)        
        self.layout_input.addWidget( self.group1 ,3 ,1 )

        self.widget_input = QWidget()
        self.widget_input.setLayout(self.layout_input)
        self.layout_stack.addWidget(self.widget_input)
        
#--------------------------------------------------------------------------
        self.layout_graph = QVBoxLayout()
        
        custom_colour_bg = QColor(240,240,255)
        pg_colour1 = pg.mkColor(custom_colour_bg)
        custom_colour_gr = QColor(0,0,128)
        pg_colour2 = pg.mkColor(custom_colour_gr)
		
        self.plot1 = pg.PlotWidget()
        self.plot1.setBackground(pg_colour1)
        self.plot1.showGrid(x=True, y=True, alpha=1.0)

        #temp1_o = pg.PlotDataItem(np.array([a for [a,b,c,d] in self.list4d_tocki[1:]], dtype=float),np.array([b for [a,b,c,d] in self.list4d_tocki[1:]], dtype=float), pen=pg.mkPen(pg_colour2, width=4), name='old')
        temp1_o = pg.PlotDataItem(np.array([1, 2, 3, 4, 5], dtype=float),np.array([30, 32, 34, 32, 33], dtype=float), pen=pg.mkPen(pg_colour2, width=4), name='f')
        self.plot1.addItem(temp1_o)

        self.button44 = QPushButton("Отчистить график")
        self.button44.clicked.connect(self.clearplot1)

        self.layout_graph.addWidget(self.plot1)
        self.layout_graph.addWidget(self.button44)
        
        self.widget_graph = QWidget()
        self.widget_graph.setLayout(self.layout_graph)
        self.layout_stack.addWidget(self.widget_graph)

#--------------------------------------------------------------------------
        self.layout_out = QGridLayout()

        self.table = QTableWidget(10, 10, self)
        for i in range(10):
            for j in range(10):
                self.table.setItem(i, j, QTableWidgetItem(f"Item {i}-{j}"))
        self.layout_out.addWidget(self.table,0,0)

        self.widget_out = QWidget()
        self.widget_out.setLayout(self.layout_out)
        self.layout_stack.addWidget(self.widget_out)
        
#-------------------------------------------------------------------------
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout_stack)
        self.setCentralWidget(self.central_widget)

#-------------------------------------------------------------------------
        self.menu = self.menuBar()
        self.viewMenu = self.menu.addMenu("Меню")
        
        self.switchAction1 = QAction("Ввод", self)
        self.switchAction1.triggered.connect(self.switch_layout_input)
        self.viewMenu.addAction(self.switchAction1)
        
        self.switchAction2 = QAction("Графики", self)
        self.switchAction2.triggered.connect(self.switch_layout_graph)
        self.viewMenu.addAction(self.switchAction2)
        
        self.switchAction3 = QAction("Результат", self)
        self.switchAction3.triggered.connect(self.switch_layout_out)
        self.viewMenu.addAction(self.switchAction3)
#===========================================================================================
    
    def switch_layout_input(self):
        self.layout_stack.setCurrentIndex(0)

    def switch_layout_graph(self):
        self.layout_stack.setCurrentIndex(1)

    def switch_layout_out(self):
        self.layout_stack.setCurrentIndex(2)
 
    def clearplot1(self):
        self.plot1.clear()
        self.plot1.showGrid(x=True, y=True, alpha=1.0)
    
    def clearandplot(self):
        self.clearplot1()
        self.myiter = 0
        print(self.myiter, "new loop idk")
        self.myplot()

   
#===========================================================================================
    def myplot(self):
        self.start1()
        pass
    
    def start1(self):
        
        self.stable_n = 0
        self.stable_N = 0
        self.unstable_n = 0
        self.unstable_N = 0

        x = sp.Symbol('x')
        y = sp.Symbol('y')
        a = sp.Symbol('a')
        a = 1.35
        h = 0.05
        h1= 0.1
        itercount = 10

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
        
        for i in range(itercount-3):
            X_current =X.subs({x: V1_x_folder[-1]*h1, y: V1_y_folder[-1]*h1})
            Y_current = Y.subs({x: V1_x_folder[-1]*h1, y: V1_y_folder[-1]*h1})
            V1_x_folder.append(X_current)
            V1_y_folder.append(Y_current)
            
        print(V1_x_folder,V1_y_folder ,"_--------------------\n\n\n\n\n")

        u = []
        self.stable_n = len(V1_x_folder)
        for i in range(len(V1_x_folder)-1):
            u = u + gen([V1_x_folder[i], V1_y_folder[i]], [V1_x_folder[i+1], V1_y_folder[i+1]])
        print("assssssssdasdas",u)
        V1_x_folder, V1_y_folder = u[0::2], u[1::2]
        self.stable_N = len(V1_x_folder)

        print(V1_x_folder, end = "\n\n")
        print(V1_y_folder, end = "\n\n")

        X=eval("x - y")
        Y=eval("y - a*(x-y)*(1-x+y)" )

        V2_x_folder = [0.0, V2[0], X.subs({x: V2[0], y: V2[1]})]
        V2_y_folder = [0.0, V2[1], Y.subs({x: V2[0], y: V2[1]})]

        for i in range(itercount-3):
            X_current =X.subs({x: V2_x_folder[-1]*h1, y: V2_y_folder[-1]*h1})
            Y_current = Y.subs({x: V2_x_folder[-1]*h1, y: V2_y_folder[-1]*h1})
            V2_x_folder.append(X_current)
            V2_y_folder.append(Y_current)

        u = []
        self.unstable_n = len(V2_x_folder)
        for i in range(len(V2_x_folder)-1):
            u = u + gen([V2_x_folder[i], V2_y_folder[i]], [V2_x_folder[i+1], V2_y_folder[i+1]])
        #print(u)
        V2_x_folder, V2_y_folder = u[0::2], u[1::2]
        self.unstable_N = len(V2_x_folder)

        print(V2_x_folder, end = "\n\n")
        print(V2_y_folder, end = "\n\n")

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
        
        ttemp1 = pg.PlotDataItem(np.array(u[0][0], dtype=float) , np.array(u[0][1], dtype=float) , 
                                                                       pen=pg.mkPen("r", width=4), name='stable')
        self.plot1.addItem(ttemp1)         
        ttemp2 = pg.PlotDataItem(np.array(u[1][0], dtype=float) , np.array(u[1][1], dtype=float) , 
                                                                       pen=pg.mkPen("black", width=4), name='unstable')
        self.plot1.addItem(ttemp2)        
        
        print(f"stable   n {  self.stable_n}   N {  self.stable_N}")
        print(f"unstable n {self.unstable_n}   N {self.unstable_N}")
        entropia = log(max([self.stable_N,self.unstable_N]))/itercount
        print(f"Энтропия {entropia}")



app = QApplication([])
window = MainWindow()
window.show()
app.exec()