
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout,
                               QPushButton, QWidget, QStackedLayout,QLineEdit,
                               QGridLayout, QLabel,QTableWidget, 
                               QTableWidgetItem,QGroupBox)
from PySide6.QtGui import QAction, QColor , QPainter, QPixmap
from PySide6.QtCore import Qt
import time
import networkx as nx
#import matplotlib.patches as patches
import math as m

#==========================================================================

def cartesian_to_qrectf(x, y, height,width):
    y_qrectf = height - y
    x_1231 = width + x
    return x_1231, y_qrectf

def my_eval(str1):
    str2 = f"lambda x, y: {str1}"
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
        self.setWindowTitle("Построение цепно-рекурентного множества")
        self.layout_stack = QStackedLayout()

#--------------------------------------------------------------------------
        self.layout_input = QGridLayout()

        self.group1 = QGroupBox("Система уравнений")
        self.group1.setMaximumSize(300, 200) 
        layout1 = QVBoxLayout()
        self.fun1 = QLineEdit( "x*x-y*y+a" )
        self.fun2 = QLineEdit( "2*x*y+b" )
        layout1.addWidget(self.fun1)
        layout1.addWidget(self.fun2)
        self.group1.setLayout(layout1)        
        self.layout_input.addWidget( self.group1 ,1 , 0)
        
        self.group1 = QGroupBox("Значения параметров")
        self.group1.setMaximumSize(300, 200) 
        layout1 = QGridLayout()
        self.pnamea = QLineEdit( "a" )
        self.pvalua = QLineEdit( "0.3" )
        self.pnameb = QLineEdit( "b" )
        self.pvalub = QLineEdit( "0.2" )
        layout1.addWidget(self.pnamea , 0 , 0 )
        layout1.addWidget(self.pvalua , 0, 1)
        layout1.addWidget(self.pnameb , 1 , 0 )
        layout1.addWidget(self.pvalub , 1, 1)
        self.group1.setLayout(layout1)        
        self.layout_input.addWidget( self.group1 ,1 ,1)
        
        self.group1 = QGroupBox("Точки задающие область")
        self.group1.setMaximumSize(300, 100) 
        layout1 = QGridLayout()
        self.dot1 = QLineEdit( " -2,-2 ")
        self.dot2 = QLineEdit( " 2,2 ")
        layout1.addWidget(self.dot1 , 0 , 0 )
        layout1.addWidget(self.dot2 , 0, 1)
        self.group1.setLayout(layout1)        
        self.layout_input.addWidget( self.group1 ,2 ,0 )
        
        self.group1 = QGroupBox("Коэфициент переразбиения и количество точек ") #    отображаемых в ячейки")
        self.group1.setMaximumSize(300, 100) 
        layout1 = QGridLayout()
        self.koefh = QLineEdit( " 0.5 ")
        self.countp = QLineEdit( " 4 ")
        layout1.addWidget(self.koefh , 0 , 0 )
        layout1.addWidget(self.countp , 0, 1)
        self.group1.setLayout(layout1)        
        self.layout_input.addWidget( self.group1 ,2 ,1 )
        
        self.group1 = QGroupBox("Построить итераций и Достроить итераций")
        self.group1.setMaximumSize(300, 200) 
        layout1 = QGridLayout()
        self.button1 = QPushButton("Построить график для итераций:")
        self.button1.clicked.connect(self.start1)
        self.globiterc1 = QLineEdit( " 6 ")
        self.button3 = QPushButton("Проитерировать существующий:")
        self.globiterc2 = QLineEdit( " 1 ")
        self.button1.clicked.connect(self.iterate_from_start)
        self.button3.clicked.connect(self.iterate_from_current)
        layout1.addWidget(self.button1 , 0, 0)

        

        layout1.addWidget(self.globiterc1 , 0, 1)
        layout1.addWidget(self.button3 , 1 , 0 )
        layout1.addWidget(self.globiterc2 , 1, 1)
        self.group1.setLayout(layout1)        
        self.layout_input.addWidget( self.group1 ,3 ,0 )
        
        self.button2 = QPushButton("Отчистить старые данные и занести новые ")
        self.button2.clicked.connect(self.start1)
        self.layout_input.addWidget( self.button2 ,3 ,1 )
        
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
        pixmap.fill(Qt.white)
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

    def start1(self):
        self.x0, self.y0 = eval( self.dot1.text())
        self.x1, self.y1 = eval( self.dot2.text())
        self.h = eval( self.koefh.text() )
        #itercount = eval(self.iterp.text())
        self.pointcounter = eval(self.countp.text())

        self.a = eval( self.pvalua.text() )
        self.b = eval( self.pvalub.text() )
        self.symb_a = str( self.pnamea.text() )
        self.symb_b = str( self.pnameb.text() )

        self.iterc = eval( self.globiterc1.text() )
        self.iterc2 = eval( self.globiterc2.text() )
        
        strxfunc =  str( self.fun1.text() )
        stryfunc =  str( self.fun2.text() )
        
        strxfunc = strxfunc.replace(self.symb_a, enc(self.a))
        strxfunc = strxfunc.replace(self.symb_b, enc(self.b))
        stryfunc = stryfunc.replace(self.symb_a, enc(self.a))
        stryfunc = stryfunc.replace(self.symb_b, enc(self.b))
        
        #print( x0, y0,  x1, y1, h ,  pointcounter, a,  symb_a,  b, symb_b, iterc, iterc2, strxfunc, stryfunc)

        self.xfunc = my_eval(strxfunc)
        self.yfunc = my_eval(stryfunc)
        self.xposition = lambda cell, leng: self.x0+self.h*(cell-(cell-1)//leng*leng-1)
        self.yposition = lambda cell, leng: self.y1-self.h*((cell-1)//leng+1)
        
        self.lengx = abs(self.x1 - self.x0) / self.h
        self.lengy = abs(self.y1 - self.y0) / self.h
        self.list_good_dots = [q for q in range(1, int(self.lengx*self.lengy))]
        self.G = nx.DiGraph()
        self.flag_from_iterate = 0
        self.flag_to_iterate = -1
        self.res_neout1 = ""

        self.mashtab = self.W_HIGHT/abs(self.y0-self.y1)

        print("start1 done")
    
    def iterate_from_start(self):
        self.start1()
        self.flag_to_iterate =  eval( self.globiterc1.text() )
        self.mainiteration()
    
    def iterate_from_current(self):
        self.flag_from_iterate = self.flag_to_iterate
        self.flag_to_iterate =  self.flag_to_iterate + eval( self.globiterc2.text() )
        self.mainiteration()
    
    def mainiteration(self):
        for gh in range(self.flag_from_iterate+1, (self.flag_to_iterate+1)):
            start_time = time.time()
            self.G = self.calculate_symbolic_representation_dynamic_system(self.x0, self.x1, self.y0, self.y1, self.h, self.lengx, self.G, self.list_good_dots, self.pointcounter)

            self.list_good_dots = list(self.G.nodes())  # номера ячеек, которые попали

            if gh ==  (self.flag_to_iterate):
                pixmap = QPixmap(self.W_HIGHT, self.W_WIDTH)
                pixmap.fill(Qt.white)

                painter = QPainter(pixmap)
                painter.setPen(QColor(255, 0, 0))#
                painter.setBrush(QColor(255, 0, 0))
                
                painter.drawRect(int(self.W_WIDTH/2), 0, 0, self.W_HIGHT) #VERTICAL
                painter.drawRect(0, int(self.W_HIGHT/2), self.W_WIDTH, 0) #HORISONTAL
                
                painter.setPen(QColor(0, 0, 0))#
                painter.setBrush(QColor(0, 0, 0))
                myh = int(self.h*self.mashtab)
                if myh<1:
                    myh = 1
                
                for c in nx.strongly_connected_components(self.G):
                    if len(c) > 1:
                        alist = list(c)
                        for k in range(0, len(alist)):
                            x,y = cartesian_to_qrectf(self.xposition(alist[k], self.lengx), self.yposition(alist[k], self.lengx),  max([self.y1,self.y0]), max([self.x1,self.x0]) )
                            #print(x,y)
                            painter.drawRect( x*self.mashtab,y*self.mashtab , myh, myh)
                
                painter.end()

                self.picture_out1.setPixmap(pixmap)
                
            self.G.clear()
            self.newbuf = self.list_good_dots
            self.list_good_dots = []
            for i in range(0, len(self.newbuf)):
                r1 = cell_dribling(self.newbuf[i], self.lengx)
                self.list_good_dots += r1
            
            self.h *= 0.5
            self.lengx *= 2
            print(gh, " iteration is done! Time elapsed: ", (time.time() - start_time))
            print( ( (self.x1-self.x0 )*(self.y1-self.y0) ) / ( self.h**2 ) )
            self.res_neout1 = self.res_neout1 + f"\n {gh} итерация. Занято времени {time.time() - start_time}\n Количество ячеек {( (self.x1-self.x0 )*(self.y1-self.y0) ) / ( self.h**2 ) }"
            if gh ==  (self.flag_to_iterate):
                self.res_neout1 = self.res_neout1 + f"   На этой итерации также был нарисован график"
                self.res_out1.setText(self.res_neout1)






    def calculate_symbolic_representation_dynamic_system(self, xdown, xup, ydown, yup, h, leng, G, s_list, pt):
        cou = 1
        xtmp = xdown
        ytmp = yup
        xckl = xdown
        yckl = yup
        cell_list = []
        while yckl > ydown:
            while xckl < xup:
                for i in range(0, pt):
                    ytmp -= 1 / pt*h

                    for j in range(0, pt):
                        xtmp += 1 / pt*h
                        
                        xrz = self.xfunc(xtmp, ytmp)
                        yrz = self.yfunc(xtmp, ytmp)

                        if xrz < xdown or xrz > xup or yrz < ydown or yrz > yup:
                            continue
                        cell = m.floor(((yup - yrz) / h)) * leng + m.ceil((xrz - xdown) / h) // 1 + 1
                        if not (cell in cell_list):   
                            cell_list.append(cell)

                    xtmp = xckl

                xckl += h
                xtmp = xckl
                ytmp = yckl
                
                for i in range(0, len(cell_list)):
                    G.add_edge(cou, cell_list[i])
                cou += 1
                cell_list.clear()
            yckl -= h
            xckl = xdown
            xtmp = xckl
            ytmp = yckl
        return G


#==========================================================
app = QApplication([])
window = MainWindow("window")
window.show()
app.exec()
