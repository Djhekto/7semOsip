from PySide6.QtWidgets import QApplication,QVBoxLayout, QGroupBox, QMainWindow, QVBoxLayout, QPushButton, QWidget, QStackedLayout,QLineEdit, QGridLayout, QLabel,QTableWidget, QTableWidgetItem
from PySide6.QtGui import QAction, QColor
from PySide6.QtCore import QSize
import numpy as np
import pyqtgraph as pg
from sympy import symbols, diff
from numpy import linalg as LA



def enc(str1):
    if type(str1)!=type("a"):        str1 = str(str1)
    return "(" + str1 + ")"

class MainWindow(QMainWindow):
    def __init__(self): 
        super(MainWindow, self).__init__()
        self.setWindowTitle("prog -997")
        self.layout_stack = QStackedLayout()

#--------------------------------------------------------------------------
        self.layout_input = QGridLayout()

        self.txt_fun1 = QLineEdit( "x + y + a*x*(1-x)" )
        self.txt_fun2 = QLineEdit( "y + a*x*(1-x)" )
        self.txt_fun1rev = QLineEdit( "x - y" )
        self.txt_fun2rev = QLineEdit( "a*(x**2) - a*x + a*(y**2) + a*y - 2*a*x*y + y" )
        self.txt_parvalue = QLineEdit( "1.35" )
        self.txt_parname = QLineEdit( "a" )
        self.txt_accvalue = QLineEdit( "0.1" )
        self.txt_symbols = QLineEdit( "x,y" )
        self.txt_iterc = QLineEdit( "10" )
        self.txt_iterp = QLineEdit( "10" )
        self.txt_start = QLineEdit( "[0,0]")
        self.txt_v1x = QLineEdit( " 2.1583123951777 ")
        self.txt_v1y = QLineEdit( " 1 ")
        self.txt_v2x = QLineEdit( " 1.1583123951777 ")
        self.txt_v2y = QLineEdit( " -1 ")

        self.button1 = QPushButton("построить график")
        self.button2 = QPushButton("[debug] загрузить данные в прогу")
        #self.button1.clicked.connect(self.postroit1)
        self.button2.clicked.connect(self.debug_read_input)
        self.button3 = QPushButton("дополнить график")


        self.group1 = QGroupBox("Система уравнений")
        self.group1.setMaximumSize(QSize(300, 200)) 
        layout1 = QVBoxLayout()
        layout1.addWidget(self.txt_fun1)
        layout1.addWidget(self.txt_fun2)
        self.group1.setLayout(layout1)        
        self.layout_input.addWidget( self.group1 ,1 , 0)

        self.group1 = QGroupBox("Обратная система уравнений")
        self.group1.setMaximumSize(QSize(300, 200)) 
        layout1 = QVBoxLayout()
        layout1.addWidget(self.txt_fun1rev)
        layout1.addWidget(self.txt_fun2rev)
        self.group1.setLayout(layout1)        
        self.layout_input.addWidget( self.group1 ,1 ,1)
        
        self.group1 = QGroupBox("Значение и символ параметра")
        self.group1.setMaximumSize(QSize(300, 100)) 
        layout1 = QGridLayout()
        layout1.addWidget(self.txt_parvalue , 0 , 0 )
        layout1.addWidget(self.txt_parname , 0, 1)
        self.group1.setLayout(layout1)        
        self.layout_input.addWidget( self.group1 ,2 ,0)
        
        self.group1 = QGroupBox("Начальная точка и точность")
        self.group1.setMaximumSize(QSize(300, 100)) 
        layout1 = QGridLayout()
        layout1.addWidget(self.txt_start , 0 , 0 )
        layout1.addWidget(self.txt_accvalue , 0, 1)
        self.group1.setLayout(layout1)        
        self.layout_input.addWidget( self.group1 ,2 ,1 )

        self.group1 = QGroupBox("Кол-во итераций посчитать сразу и по кнопке")
        self.group1.setMaximumSize(QSize(300, 200)) 
        layout1 = QGridLayout()
        layout1.addWidget(self.txt_iterc , 0 , 0 )
        layout1.addWidget(self.txt_iterp , 0, 1)
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
        layout1.addWidget(self.txt_v1x , 1 , 0 )
        layout1.addWidget(self.txt_v1y , 2, 0)
        layout1.addWidget(self.txt_v2x , 1 , 1 )
        layout1.addWidget(self.txt_v2y , 2, 1)
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

        self.button3 = QPushButton("Отчистить график")
        self.button3.clicked.connect(self.clearplot1)

        self.layout_graph.addWidget(self.plot1)
        self.layout_graph.addWidget(self.button3)
        
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

    def switch_layout_input(self):
        self.layout_stack.setCurrentIndex(0)

    def switch_layout_graph(self):
        self.layout_stack.setCurrentIndex(1)

    def switch_layout_out(self):
        self.layout_stack.setCurrentIndex(2)
 
    def clearplot1(self):
        self.plot1.clear()
        self.plot1.showGrid(x=True, y=True, alpha=1.0)

    def debug_read_input(self):
        print("knopka")
        str_fun1 =  self.txt_fun1.text()
        str_fun2 =  self.txt_fun2.text()
        str_fun1rev = self.txt_fun1rev.text()
        str_fun2rev = self.txt_fun2rev.text()
        str_accvalue = self.txt_accvalue.text()
        str_iterc =  self.txt_iterc.text()
        str_iterp =  self.txt_iterp.text()
        
        str_start = eval( self.txt_start.text())
        symbols = []
        for ii,elem in enumerate( self.txt_symbols.text().split(",")):
             symbols.append(elem)
        print( symbols,  str_start)
        
        df1_dx = diff( str_fun1,  symbols[0])
        df1_dy = diff( str_fun1,   symbols[1])
        df2_dx = diff( str_fun2,   symbols[0])
        df2_dy = diff( str_fun2,   symbols[1])
        Df_const = [[df1_dx,df1_dy],[df2_dx,df2_dy]]
        print( Df_const)
        
        str_parvalue =  self.txt_parvalue.text()
        str_parname =  self.txt_parname.text()
        print( str_parvalue,  str_parname)
        
        Df =  Df_const
        for i, ilist in enumerate(Df):
            for ii,iielem in enumerate(ilist):
                for iii,symb in enumerate( symbols):
                    Df[i][ii] = str(Df[i][ii]).replace(symb, enc( str_start[iii]))
                Df[i][ii] = eval(Df[i][ii].replace( str_parname, enc( str_parvalue)))
                print(Df[i][ii])
        
        print(Df)
    
    def vova_kod(self):
        eps = 0.01
        eps0 = 5e-7
        DF = [[2.35, 1],[1.35,1]]
        w, v = LA.eig(DF)

        Vu = v[:,0]     # unstable manifold
        Vs = v[:,1]     # stable manifold
        
        # Plot the unstable manifold
        Hr = np.zeros(shape=(100,150))
        Ht = np.zeros(shape=(100,150))
        for eloop in range(0,100):

            eps = eps0*eloop

            x_n0 = eps*Vu[0]
            y_n0 = eps*Vu[1]

            Nloop = np.ceil(-6*np.log(eps0)/np.log(eloop+2))
            flag = 1
            cnt = 0

            while flag==1 and cnt < Nloop:
                # тут менять формулу надо 
                # стандарт мэп (Чириков)
                x_n1=x_n0+y_n0+1.35*x_n0*(1-x_n0)
                y_n1=y_n0+1.35*x_n0*(1-x_n0)

                x_n0 = x_n1
                y_n0 = y_n1

                if y_n1 > 4*np.pi:
                    flag = 0

                Hr[eloop,cnt] = x_n0
                Ht[eloop,cnt] = y_n0
                cnt = cnt+1

        # x = Hr[0:11,12]
        # y = Ht[0:11,12]
        x = Hr[0:99,12]
        y = Ht[0:99,12]

        # Plot the stable manifold
        del Hr, Ht
        del x,y
        Hr = np.zeros(shape=(100,150))
        Ht = np.zeros(shape=(100,150))

        for eloop in range(0,100):
            eps = eps0*eloop
        
            x_n0 = eps*0.83125573
            y_n0 = eps*(-0.4438839)

            Nloop = np.ceil(-6*np.log(eps0)/np.log(eloop+2))
            flag = 1
            cnt = 0

            while flag==1 and cnt < Nloop:
                
                x_n1=x_n0-y_n0
                y_n1=y_n0-1.35*x_n1*(1-x_n1)

                x_n0 = x_n1
                y_n0 = y_n1
                
                if y_n1 > 4*np.pi:
                    flag = 0 
                Hr[eloop,cnt] = x_n0
                Ht[eloop,cnt] = y_n0
                cnt = cnt+1

        # x = Hr[0:9,12]
        # y = Ht[0:9,12]
        x = Hr[0:79,12]
        y = Ht[0:79,12]






app = QApplication([])
window = MainWindow()
window.show()
app.exec()
#window.vova_kod()


"""
        self.sup1 = QLabel()
        self.sup1.setText("Система уравнений"); self.sup1.setMaximumSize(QSize(200, 10))
        self.sup2 = QLabel()
        self.sup2.setText("Обратная система уравнений"); self.sup2.setMaximumSize(QSize(200, 10))
        self.sup3 = QLabel()
        self.sup3.setText("Значение параметра"); self.sup3.setMaximumSize(QSize(200, 10))
        self.sup4 = QLabel()
        self.sup4.setText("Буква праметра"); self.sup4.setMaximumSize(QSize(200, 10))
        self.sup5 = QLabel()
        self.sup5.setText("Точность:"); self.sup5.setMaximumSize(QSize(200, 10))
        self.sup6 = QLabel()
        self.sup6.setText("Символы:"); self.sup6.setMaximumSize(QSize(200, 10))
        self.sup7 = QLabel()
        self.sup7.setText("Кол-во итераций"); self.sup7.setMaximumSize(QSize(200, 10))
        self.sup8 = QLabel()
        self.sup8.setText("Кол-во итераций построить"); self.sup8.setMaximumSize(QSize(200, 10))
        self.sup9 = QLabel()
        self.sup9.setText("Значение вектора начальной точки:"); self.sup9.setMaximumSize(QSize(200, 10))
"""