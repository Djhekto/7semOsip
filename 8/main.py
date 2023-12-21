
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout,
                               QPushButton, QWidget, QStackedLayout,QLineEdit,
                               QGridLayout, QLabel,QTableWidget, QCheckBox,
                               QTableWidgetItem,QGroupBox)
from PyQt6.QtGui import QAction, QColor , QPainter, QPixmap
from PyQt6.QtCore import Qt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.colors import Normalize

import time
import networkx as nx
import math as m
from math import cos,sin, pi, sqrt
import numpy as np
from numpy.linalg import eig
from sympy import Symbol, expand

#==========================================================================

def cartesian_to_qrectf(x, y, height,width):
    y_qrectf = height - y
    x_1231 = width + x
    return x_1231, y_qrectf

def my_eval(str1):
    str2 = f"lambda x, y: {str1}"
    return eval(str2)

def my_eval_with_t(str1):
    x = Symbol("x")
    y = Symbol("y")
    t = Symbol("t")
    sssstr = expand(str1)
    print(str(sssstr))
    str2 = f"lambda x, y, t: {str(sssstr)}"
    #str2 = f"lambda x, y, t: {str1}"
    return eval(str2)

def enc(str1):
    if type(str1)!=type("a"):        str1 = str(str1)
    return "(" + str1 + ")"

def cell_dribling(item, leng):
    lengnew = leng*2
    new1 = 2*item-1+(item-1)//leng*lengnew
    new2 = new1+1
    new3 = new1+lengnew
    new4 = new2+lengnew
    return [new1, new2, new3, new4]

#==========================================================================

class MainWindow(QMainWindow):
    
    def __init__(self,name11):
        super(MainWindow, self).__init__()
        self.name = name11
        self.setWindowTitle("Усреднение функции")
        self.layout_stack = QStackedLayout()

#--------------------------------------------------------------------------
        self.layout_input = QGridLayout()

        self.group1 = QGroupBox("Система уравнений")
        self.group1.setMaximumSize(300, 200) 
        layout1 = QGridLayout()
        self.funlabel1 = QLabel("f = ")
        self.funlabel2 = QLabel("g = ")        
        self.fun1 = QLineEdit( "  x*x-y*y+a " )
        self.fun2 = QLineEdit( " - 2*x*y+b " )
        layout1.addWidget(self.funlabel1,0,0)
        layout1.addWidget(self.funlabel2,1,0)
        layout1.addWidget(self.fun1,0,1)
        layout1.addWidget(self.fun2,1,1)
        self.group1.setLayout(layout1)        
        self.layout_input.addWidget( self.group1 ,1 , 0)

        self.group1 = QGroupBox("Параметры")
        self.group1.setMaximumSize(300, 200) 
        layout1 = QGridLayout()
        self.labelparam = QLabel("Параметры уравнения ")
        self.listparam = QLineEdit( " a=0.3,b=0.2 " )
        layout1.addWidget(self.labelparam,0,0)
        layout1.addWidget(self.listparam,0,1)        
        self.labelobl = QLabel("Область ")
        self.txtobl = QLineEdit( " [-2,-2]x[2,2] " )
        layout1.addWidget(self.labelobl,1,0)
        layout1.addWidget(self.txtobl,1,1)               
        self.group1.setLayout(layout1)        
        self.layout_input.addWidget( self.group1 ,1 , 1)
        
        self.group1.setLayout(layout1)        
        self.layout_input.addWidget( self.group1 ,1 , 0)

        self.group1 = QGroupBox("Построить итераций и Достроить итераций")
        self.group1.setMaximumSize(300, 200) 
        layout1 = QGridLayout()
        self.button1 = QPushButton("Построить график для итераций:")
        self.globiterc1 = QLineEdit( " 9 ")
        self.button1.clicked.connect(self.iterate_from_start)
        #self.button3 = QPushButton("[x]Проитерировать существующий:")
        #self.globiterc2 = QLineEdit( " 1 ")
        #self.button3.clicked.connect(self.iterate_from_current)
        layout1.addWidget(self.button1 , 0, 0)
        layout1.addWidget(self.globiterc1 , 0, 1)
        #layout1.addWidget(self.button3 , 1 , 0 )
        #layout1.addWidget(self.globiterc2 , 1, 1)
        self.button44 = QPushButton("Построить изображение")
        self.button44.clicked.connect(self.mymainpainter)
        layout1.addWidget(self.button44 , 2, 0)
        self.group1.setLayout(layout1)        
        self.layout_input.addWidget( self.group1 ,2 ,0 )
        
        self.group1 = QGroupBox("Функция оснащения")
        self.group1.setMaximumSize(300, 200) 
        layout1 = QGridLayout()
        self.labelextra= QLabel("φ(x,y) = ")
        layout1.addWidget(self.labelextra,0,0)
        self.txtfunnn = QLineEdit( "x*x+y*y" )
        layout1.addWidget(self.txtfunnn,0,1)
        self.extradefault = False
        self.group1.setLayout(layout1)        
        self.layout_input.addWidget( self.group1 ,2 , 1)
        
        self.widget_input = QWidget()
        self.widget_input.setLayout(self.layout_input)
        self.layout_stack.addWidget(self.widget_input)
        
#--------------------------------------------------------------------------
        self.layout_graph = QVBoxLayout()
        
        self.W_HIGHT = 700
        self.W_WIDTH = 700
		
        self.picture_out1 = QLabel()
        self.picture_out1.setMinimumSize(self.W_WIDTH, self.W_HIGHT)
        self.layout_graph.addWidget( self.picture_out1)
        
        pixmap = QPixmap(self.W_HIGHT, self.W_WIDTH)
        pixmap.fill(QColor(255, 255, 255))
        self.picture_out1.setPixmap(pixmap)

        self.widget_graph = QWidget()
        self.widget_graph.setLayout(self.layout_graph)
        self.layout_stack.addWidget(self.widget_graph)

#--------------------------------------------------------------------------
        self.layout_out = QGridLayout()

        self.res_out1 = QLabel()
        self.res_neout1 = ""
        self.res_out1.setText(f"Количество ячеек,\n Время итерации")
        self.layout_out.addWidget( self.res_out1)

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

    def switch_layout_input(self):
        self.layout_stack.setCurrentIndex(0)

    def switch_layout_graph(self):
        self.layout_stack.setCurrentIndex(1)

    def switch_layout_out(self):
        self.layout_stack.setCurrentIndex(2)
    #==========================================================
    def extraaction(self):
        print("--")
        if self.extradefault:
            self.extradefault = False
            print("tofalse")
        else:
            print("totrue")
            self.extradefault = True
        
    def iterate_from_start(self):
        self.iternum = int(self.globiterc1.text())
        self.res_neout1 = ""
        self.mainiteration()
    
    def iterate_from_current(self):
        self.iternum += int(self.globiterc2.text())
        self.mainiteration()
    
    def draw_3d_bar(self):
        _x = np.arange(4)
        _y = np.arange(3)
        _xx, _yy = np.meshgrid(_x, _y)
        _x, _y = _xx.ravel(), _yy.ravel()

        _z = np.zeros_like(_x)
        _dx = _dy = np.ones_like(_z)
        _dz = [1, 2, 3, 4, 2, 3, 4, 2, 5, 7, 2, 1]

        self.axis.bar3d(_x, _y, _z, _dx, _dy, _dz)
        self.canvas.draw()
        
    def mainiteration(self):
        somelist1, somelist2 = (self.txtobl.text()).split("x")
        somelist1 = eval(str(somelist1))
        somelist2 = eval(str(somelist2))
        x0 = somelist1[0]
        y0 = somelist2[1]
        L = somelist2[0] - somelist1[0]
        H = somelist2[1] - somelist1[1]
        print(x0,y0,L,H)
        somelist1, somelist2 = (self.listparam.text()).split(",")
        a = str(somelist1).split("=")[1]
        b = str(somelist2).split("=")[1]
        print(a,b)
        iterations = self.globiterc1.text()
        #if self.iternum == int(self.globiterc1.text()):
            #self.res_neout1 = f"{matr}\nСобственные значения: {eig(matr)[0][0]} {eig(matr)[0][1]} {eig(matr)[0][2]}\n"
        self.start = time.time()
        os.system(f".\main.exe {x0} {y0} {L} {H} {a} {b} {iterations}") # {a32} {a33} {self.iternum}")  
        #os.system(f".\main.exe {a11} {a12} {a13} {a21} {a22} {a23} {a31} {a32} {a33} {self.iternum}")    
        
    def mymainpainter(self):       
        with open('res.txt') as f:
            lines = f.readlines()

        print(lines[-1])
        print(lines[-2])
        print(lines[-3])
        toprintdiam = lines[-3]
        toprintcoms = lines[-2]
        toprintnumc = lines[-1]
        #toprintcomsnum = lines[-1].rstrip()
        #toprintcellamount = lines[-2].split(" ")[1].rstrip()
        #toprintentropy = lines[-3].rstrip()
        #toprintloglambda = lines[-4].rstrip()
        #self.res_neout1 = f"{self.res_neout1}Время подсчета { self.iternum } итераций: {restime}\nРазмер ячейки: {d}\n"
        lines = lines[:-3]
        celllist = lines

        pixmap = QPixmap(self.W_HIGHT, self.W_WIDTH)
        pixmap.fill(QColor(255, 255, 255))

        painter = QPainter(pixmap)
        painter.setPen(QColor(255, 0, 0))#
        painter.setBrush(QColor(255, 0, 0))
        
        painter.drawRect(int(self.W_WIDTH/2), 0, 0, self.W_HIGHT) #VERTICAL
        painter.drawRect(0, int(self.W_HIGHT/2), self.W_WIDTH, 0) #HORISONTAL
        
        painter.setPen(QColor(0, 0, 0))#
        painter.setBrush(QColor(0, 0, 0))
        
        self.x0 = -2
        self.x1 = 2
        self.y0 = -2
        self.y1 = 2
        self.h = float(toprintdiam)
        self.mashtab = self.W_HIGHT/abs(self.y0-self.y1)
        print(self.mashtab)
        self.xposition = lambda cell, leng: self.x0+self.h*(cell-(cell-1)//leng*leng-1)
        self.yposition = lambda cell, leng: self.y1-self.h*((cell-1)//leng+1)
        self.lengx = abs(self.x1 - self.x0) / self.h

        for e in celllist:
            e = eval(e)
            #print(e,self.lengx)
            x,y = cartesian_to_qrectf(self.xposition(e, self.lengx), self.yposition(e, self.lengx),  max([self.y1,self.y0]), max([self.x1,self.x0]))
            #print(x,y)
            painter.drawRect( int(x*self.mashtab), int(y*self.mashtab) ,int(self.h*self.mashtab), int(self.h*self.mashtab))
        painter.end()
        self.picture_out1.setPixmap(pixmap)

        try:
            restime = time.time() - self.start
        except AttributeError:
            restime = 0
            self.iternum = 0
        print(restime)
        self.res_neout1 = f"{self.res_neout1}Время подсчета { self.iternum } итераций: {restime}\nРазмер ячейки: {toprintdiam}\n"
        self.res_neout1 = f"{self.res_neout1}Количество ячеек { toprintnumc }\n Компонент сильной связности: {toprintcoms}\n"
        #self.res_neout1 = f"{self.res_neout1}Энтропия: { toprintentropy }\n ln(lambda): { toprintloglambda }\n"
        
        with open('res1.txt') as f:
            lines = f.readlines()

        for i,line in enumerate(lines):
            eee = line.split(" ; ")
            self.res_neout1 = f"{self.res_neout1}Для компоненты {i+1}\nЛучшее нижнее значение { eee[0] } Лучшее верхнее значение {eee[1]}\n"

        self.res_out1.setText(self.res_neout1)


                    
#==========================================================
app = QApplication([])
window = MainWindow("window")
window.show()
app.exec()
