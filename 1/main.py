from PySide6.QtWidgets import QApplication,QVBoxLayout, QGroupBox, QMainWindow, QVBoxLayout, QPushButton, QWidget, QStackedLayout,QLineEdit, QGridLayout, QLabel,QTableWidget, QTableWidgetItem
from PySide6.QtGui import QAction, QColor
from PySide6.QtCore import QSize
import numpy as np
import pyqtgraph as pg
from numpy import linalg as LA
from sympy import Symbol, diff, expand, Matrix



def enc(str1):
    if type(str1)!=type("a"):        str1 = str(str1)
    return "(" + str1 + ")"

class MainWindow(QMainWindow): 
    myiter = 0
    
    def __init__(self): 
        super(MainWindow, self).__init__()
        self.setWindowTitle("prog -997")
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
        self.iterc = QLineEdit( "10" )
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
        print(self.myiter)
        
        symbols = [];         
        str_start = [float(elem) for elem in eval( self.start.text())]
        for ii,elem in enumerate( self.symbols.text().split(",")):
             symbols.append(elem)
        print( symbols,  str_start)
        x = Symbol(symbols[0]); y = Symbol(symbols[1])
        print( x,  y)        
        
        str_parvalue =  self.parvalue.text()
        str_parname =  self.parname.text()
        str_fun1 =  str(expand(self.fun1.text().replace( str_parname, enc( str_parvalue))))
        str_fun2 =  str(expand(self.fun2.text().replace( str_parname, enc( str_parvalue))))
        str_fun1rev = str(expand(self.fun1rev.text().replace( str_parname, enc( str_parvalue))))
        str_fun2rev = str(expand(self.fun2rev.text().replace( str_parname, enc( str_parvalue))))
        print( str_fun1,  str_fun2, str_fun1rev,  str_fun2rev,
              #type(str_fun1), 
              sep= "\n" )

        to4ki = [[str_start[0],str_start[1],str_start[0],str_start[1]]]
        #to4ki.append([0,0,0,0]) 
        to4ki.append([float(self.v1x.text()),float(self.v1y.text()),
                      float(self.v2x.text()),float(self.v2y.text())])
        print(to4ki)

        
        str_accvalue = self.accvalue.text()
        str_iterc =  self.iterc.text()
        str_iterp =  self.iterp.text()
        
        
        
        
        pass

app = QApplication([])
window = MainWindow()
window.show()
app.exec()
#window.vova_kod()
