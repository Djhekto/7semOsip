import math
from PySide6.QtWidgets import QApplication,QVBoxLayout, QGroupBox, QMainWindow, QVBoxLayout, QPushButton, QWidget, QStackedLayout,QLineEdit, QGridLayout, QLabel,QTableWidget, QTableWidgetItem
from PySide6.QtGui import QAction, QColor
from PySide6.QtCore import QSize
import numpy as np
import pyqtgraph as pg
from numpy import linalg as LA
#from sympy import Symbol, diff, expand, Matrix

from math import log
import timeit

import sympy as sp
import math as ms
from scipy.spatial import distance

class MainWindow(QMainWindow): 
    myiter = 0
    
    def __init__(self): 
        super(MainWindow, self).__init__()
        self.setWindowTitle("Henon entropy")
        self.layout_stack = QStackedLayout()

#--------------------------------------------------------------------------
        self.layout_input = QGridLayout()

        self.fun1 = QLineEdit( "1 + y - a*x*x" )
        self.fun2 = QLineEdit( "b*x" )
        self.parvalue = QLineEdit( "1.4" )
        self.parvalue2 = QLineEdit( "0.3" )
        self.parname = QLineEdit( "a" )
        self.parname2 = QLineEdit( "b" )
        self.accvalue = QLineEdit( "0.05" )
        self.preaccvalue = QLineEdit( "0.5" )
        self.iterp = QLineEdit( "15" )
        self.start = QLineEdit( "[0.1,0.1]")
        self.vvv1 = QLineEdit( "0.6" )
        self.vvv2 = QLineEdit( "0.6" )

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

        self.group1 = QGroupBox("------------------------")
        self.group1.setMaximumSize(QSize(300, 200)) 
        layout1 = QVBoxLayout()
        #layout1.addWidget(self.fun1rev)
        #layout1.addWidget(self.fun2rev)
        self.group1.setLayout(layout1)        
        self.layout_input.addWidget( self.group1 ,1 ,1)
        
        self.group1 = QGroupBox("Значение и символ параметра")
        self.group1.setMaximumSize(QSize(300, 100)) 
        layout1 = QGridLayout()
        layout1.addWidget(self.parvalue , 0 , 0 )
        layout1.addWidget(self.parname , 0, 1)
        layout1.addWidget(self.parvalue2 , 1 , 0 )
        layout1.addWidget(self.parname2 , 1, 1)
        self.group1.setLayout(layout1)        
        self.layout_input.addWidget( self.group1 ,2 ,0)
        
        self.group1 = QGroupBox("Начальная точка и точность")
        self.group1.setMaximumSize(QSize(300, 100)) 
        layout1 = QGridLayout()
        layout1.addWidget(self.start , 0 , 0 )
        layout1.addWidget(self.accvalue , 0, 1)
        self.group1.setLayout(layout1)        
        self.layout_input.addWidget( self.group1 ,2 ,1 )

        self.group1 = QGroupBox("Изначальные итерации и точность")
        self.group1.setMaximumSize(QSize(300, 200)) 
        layout1 = QGridLayout()
        layout1.addWidget(self.iterp , 0, 0)
        layout1.addWidget(self.preaccvalue , 0, 1)
        layout1.addWidget(self.button1 , 1 , 0 )
        layout1.addWidget(self.button3 , 1, 1)
        self.group1.setLayout(layout1)        
        self.layout_input.addWidget( self.group1 ,3 ,0 )

        self.group1 = QGroupBox("---------------------")
        self.group1.setMaximumSize(QSize(300, 200)) 
        layout1 = QGridLayout()
        bsup1 = QLabel("вектор"); bsup1.setMaximumSize(QSize(200, 10))
        layout1.addWidget(bsup1 , 0 , 0 )
        layout1.addWidget(self.vvv1 , 1 , 0 )
        layout1.addWidget(self.vvv2 , 2, 0)
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
        self.layout_out = QVBoxLayout()

        self.label111 = QLabel(f"точка: \nЭнтропия: ")
        self.layout_out.addWidget(self.label111 )
        
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
        
        start_time = timeit.default_timer()
        
        self.stable_n = 0
        self.stable_N = 0

        x = sp.Symbol('x')
        y = sp.Symbol('y')
        a_s = sp.Symbol(self.parname.text())
        b_s = sp.Symbol(self.parname2.text())
        a = eval( self.parvalue.text())
        b = eval( self.parvalue2.text())
        
        h = eval( self.accvalue.text() )
        h1= eval(  self.preaccvalue.text() )
        itercount = eval(self.iterp.text())
        vstart = [float(e) for e in eval(self.start.text()) ]

        X=eval(self.fun1.text())
        Y=eval(self.fun2.text())

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

        def get_angle(line1, line2):
            d1 = (line1[1][0] - line1[0][0], line1[1][1] - line1[0][1])
            d2 = (line2[1][0] - line2[0][0], line2[1][1] - line2[0][1])
            p = d1[0] * d2[0] + d1[1] * d2[1]
            n1 = math.sqrt(d1[0] * d1[0] + d1[1] * d1[1])
            n2 = math.sqrt(d2[0] * d2[0] + d2[1] * d2[1])
            ang = math.acos(p / (n1 * n2))
            ang = math.degrees(ang)
            return ang

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

        vv1_ = eval( self.vvv1.text())
        vv2_ = eval( self.vvv2.text())
        
        V1_x_folder = [ X.subs({x: vstart[0],  y: vstart[1] }) ]
        V1_y_folder = [ Y.subs({x: vstart[0],  y: vstart[1] }) ]
        
        print(V1_x_folder,V1_y_folder ,"_--------------------\n\n\n\n\n")
        
        for i in range(itercount-1):
            #X_current =X.subs({x: V1_x_folder[-1]*h1, y: V1_y_folder[-1]*h1})
            #Y_current = Y.subs({x: V1_x_folder[-1]*h1, y: V1_y_folder[-1]*h1})
            #Df[i][ii] = str(Df[i][ii]).replace(symb, enc( str_start[iii]))
            X_current = self.fun1.text().replace(str(x), str(V1_x_folder[-1]) )
            X_current = X_current.replace(str(y), str(V1_y_folder[-1]) )
            X_current = X_current.replace(str(a_s), str(a) )
            X_current = X_current.replace(str(b_s), str(b) )
            X_current = V1_x_folder[-1] + h1* eval(X_current)
            print(X_current, i, end=" ")
            
            Y_current = self.fun2.text().replace(str(x), str(V1_x_folder[-1]) )
            Y_current = Y_current.replace(str(y), str(V1_y_folder[-1]) )
            Y_current = Y_current.replace(str(a_s), str(a) )
            Y_current = Y_current.replace(str(b_s), str(b) )
            Y_current = V1_x_folder[-1] + h1* eval(Y_current)
            print(Y_current)
            
            V1_x_folder.append(X_current)
            V1_y_folder.append(Y_current)
            
        print(V1_x_folder,V1_y_folder ,"_--------------------\n\n\n\n\n")

        u = []
        self.stable_n = len(V1_x_folder)
        for i in range(len(V1_x_folder)-1):
            u = u + gen([V1_x_folder[i], V1_y_folder[i]], [V1_x_folder[i+1], V1_y_folder[i+1]])
        #print("assssssssdasdas",u)
        V1_x_folder, V1_y_folder = u[0::2], u[1::2]
        self.stable_N = len(V1_x_folder)

        print(V1_x_folder, end = "\n\n")
        print(V1_y_folder, end = "\n\n")
        print("dsadasdkjashdgashgdhasgkdhgashk")
        
        custom_colour_bg = QColor(0, 0, 139)
        darkbluecolor = pg.mkColor(custom_colour_bg)
        custom_colour_bg =  QColor(255, 165, 0)
        orangecolor = pg.mkColor(custom_colour_bg)
        
        ttemp1 = pg.PlotDataItem(np.array(V1_x_folder, dtype=float) , np.array(V1_y_folder, dtype=float) , 
                                                                       pen=pg.mkPen(darkbluecolor, width=3), name='stable')
        self.plot1.addItem(ttemp1)       
        
        print(f"stable   n {  self.stable_n}   N {  self.stable_N}")
        entropia = log(self.stable_N )/itercount
        print(f"Энтропия {entropia}")
        #print(u)
        #print(u[0][0][-1],u[0][1][-1])

        end_time = timeit.default_timer()
        execution_time = end_time - start_time        
        print(f"Program executed in: {execution_time} seconds")
        self.label111.setText(f"entropia = log({self.stable_N })/{itercount}\nЭнтропия: {entropia} \nВремя исполнения{execution_time}")



app = QApplication([])
window = MainWindow()
window.show()
app.exec()









