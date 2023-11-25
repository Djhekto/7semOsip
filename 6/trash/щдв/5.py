
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout,
                               QPushButton, QWidget, QStackedLayout,QLineEdit,
                               QGridLayout, QLabel,QTableWidget, 
                               QTableWidgetItem,QGroupBox)
from PySide6.QtGui import QAction, QColor , QPainter, QPixmap
from PySide6.QtCore import Qt
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
        self.setWindowTitle("Локализация цепно-рекурентного множества в проективном пространстве")
        self.layout_stack = QStackedLayout()

#--------------------------------------------------------------------------
        self.layout_input = QGridLayout()

        self.group1 = QGroupBox("Матрица")# 1 -1 1  1 1 -1  2 -1 0
        self.group1.setMaximumSize(300, 200) 
        layout1 = QGridLayout()
        #self.mlabel1 = QLabel("a11 =")
        self.mline1 = QLineEdit( " 1 " )
        layout1.addWidget(self.mline1,0,0)
        self.mline2 = QLineEdit( " -1 " )
        layout1.addWidget(self.mline2,0,1)
        self.mline3 = QLineEdit( " 1 " )
        layout1.addWidget(self.mline3,0,2)
        #self.mlabel1 = QLabel("a11 =")
        self.mline1n = QLineEdit( " 1 " )
        layout1.addWidget(self.mline1n,1,0)
        self.mline2n = QLineEdit( " 1 " )
        layout1.addWidget(self.mline2n,1,1)
        self.mline3n = QLineEdit( " -1 " )
        layout1.addWidget(self.mline3n,1,2)   
        #self.mlabel1 = QLabel("a11 =")
        self.mline1nn = QLineEdit( " 2 " )
        layout1.addWidget(self.mline1nn,2,0)
        self.mline2nn = QLineEdit( " -1 " )
        layout1.addWidget(self.mline2nn,2,1)
        self.mline3nn = QLineEdit( " 0 " )
        layout1.addWidget(self.mline3nn,2,2)             
        self.group1.setLayout(layout1)        
        self.layout_input.addWidget( self.group1 ,1 , 0)

        self.group1 = QGroupBox("Построить итераций и Достроить итераций")
        self.group1.setMaximumSize(300, 200) 
        layout1 = QGridLayout()
        self.button1 = QPushButton("Построить график для итераций:")
        self.globiterc1 = QLineEdit( " 8 ")
        self.button3 = QPushButton("Проитерировать существующий:")
        self.globiterc2 = QLineEdit( " 1 ")
        self.button1.clicked.connect(self.iterate_from_start)
        self.button3.clicked.connect(self.iterate_from_current)
        layout1.addWidget(self.button1 , 0, 0)
        layout1.addWidget(self.globiterc1 , 0, 1)
        layout1.addWidget(self.button3 , 1 , 0 )
        layout1.addWidget(self.globiterc2 , 1, 1)
        self.button44 = QPushButton("Построить изображение")
        self.button44.clicked.connect(self.mymainpainter)
        layout1.addWidget(self.button44 , 2, 0)
        self.group1.setLayout(layout1)        
        self.layout_input.addWidget( self.group1 ,1 ,1 )
        
        self.widget_input = QWidget()
        self.widget_input.setLayout(self.layout_input)
        self.layout_stack.addWidget(self.widget_input)
        
#--------------------------------------------------------------------------
        self.layout_graph = QGridLayout()
        
        self.W_HIGHT = 300
        self.W_WIDTH = 300
		
        self.picture_out1 = QLabel()
        self.picture_out1.setMinimumSize(self.W_WIDTH, self.W_HIGHT)
        self.layout_graph.addWidget( self.picture_out1, 0,0)        
        pixmap = QPixmap(self.W_HIGHT, self.W_WIDTH)
        pixmap.fill(Qt.white)
        self.picture_out1.setPixmap(pixmap)

        self.picture_out2 = QLabel()
        self.picture_out2.setMinimumSize(self.W_WIDTH, self.W_HIGHT)
        self.layout_graph.addWidget( self.picture_out2, 0 ,1)
        pixmap = QPixmap(self.W_HIGHT, self.W_WIDTH)
        pixmap.fill(Qt.white)
        self.picture_out2.setPixmap(pixmap)

        self.picture_out3 = QLabel()
        self.picture_out3.setMinimumSize(self.W_WIDTH, self.W_HIGHT)
        self.layout_graph.addWidget( self.picture_out3, 0 ,2)
        pixmap = QPixmap(self.W_HIGHT, self.W_WIDTH)
        pixmap.fill(Qt.white)
        self.picture_out3.setPixmap(pixmap)

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
    def iterate_from_start(self):
        self.iternum = int(self.globiterc1.text())
        self.res_neout1 = ""
        self.mainiteration()
    
    def iterate_from_current(self):
        self.iternum += int(self.globiterc2.text())
        self.mainiteration()
    
    def mainiteration(self):
        a11 = round(eval(self.mline1.text()), 3)
        a12 = round(eval(self.mline2.text()), 3)
        a13 = round(eval(self.mline3.text()), 3)
        a21 = round(eval(self.mline1n.text()), 3)
        a22 = round(eval(self.mline2n.text()), 3)
        a23 = round(eval(self.mline3n.text()), 3)
        a31 = round(eval(self.mline1nn.text()), 3)
        a32 = round(eval(self.mline2nn.text()), 3)
        a33 = round(eval(self.mline3nn.text()), 3)
        
        matr = np.array([[a11, a12, a13], [a21, a22, a23], [a31, a32, a33]])
        if self.iternum == int(self.globiterc1.text()):
            print(matr)
            print(f" собственные значения {eig(matr)[0]}")
            self.res_neout1 = f"{matr}\nСобственные значения: {eig(matr)[0][0]} {eig(matr)[0][1]} {eig(matr)[0][2]}\n"
        self.start = time.time()
        
        os.system(f".\main.exe {a11} {a12} {a13} {a21} {a22} {a23} {a31} {a32} {a33} {self.iternum}")
    
    def mymainpainter(self):
        xmax = 1
        xmin =-1
        ymax = 1
        ymin =-1
        self.W_WIDTH2 = self.W_WIDTH/2
        self.W_HIGHT2 = self.W_HIGHT/2
        
        for i in range(1,4):
            pixmap = QPixmap(self.W_HIGHT, self.W_WIDTH)
            pixmap.fill(Qt.white)
            painter = QPainter(pixmap)
            painter.setPen(QColor(255, 0, 0))#
            painter.setBrush(QColor(255, 0, 0))

            painter.drawRect(int(self.W_WIDTH/2), 0, 0, self.W_HIGHT) #VERTICAL
            painter.drawRect(0, int(self.W_HIGHT/2), self.W_WIDTH, 0) #HORISONTAL
            
            painter.setPen(QColor(0, 0, 0))#
            painter.setBrush(QColor(0, 0, 0))
            
            with open(f"{i}buf", 'r') as fd:
                for line in fd.readlines():
                    x, y, d = map(float, line.split())
                    d2 = d*self.W_WIDTH2
                    if d2<1:
                        d2 = 1
                    x = int((-xmin+x)*self.W_WIDTH2)
                    y = int((ymax-y)*self.W_HIGHT2)
                    
                    #x,y = cartesian_to_qrectf(x, y,  d, d)
                    #print(x,y)
                    painter.drawRect( x ,y , d2, d2)

                    #ss = patches.Rectangle((x, y), d, d)
                    #ax.add_patch(ss)    
                painter.end()
            if i == 1:
                self.picture_out1.setPixmap(pixmap)
            if i == 2:
                self.picture_out2.setPixmap(pixmap)
            if i == 3:
                self.picture_out3.setPixmap(pixmap)
        
        restime = time.time() - self.start
        print(restime)
        self.res_neout1 = f"{self.res_neout1}Время подсчета { self.iternum } итераций: {restime}\nРазмер ячейки: {d}\n"
        self.res_out1.setText(self.res_neout1)


#==========================================================
app = QApplication([])
window = MainWindow("window")
window.show()
app.exec()
