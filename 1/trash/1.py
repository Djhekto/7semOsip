from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QStackedLayout,QLineEdit, QGridLayout, QLabel,QTableWidget, QTableWidgetItem
from PySide6.QtGui import QAction, QColor
import numpy as np
import pyqtgraph as pg
from sympy import symbols, diff

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
        self.txt_iterc = QLineEdit( "1000" )
        self.txt_iterp = QLineEdit( "1000" )
        self.txt_start = QLineEdit( "[0,0]")

        self.sup1 = QLabel()
        self.sup1.setText("Система уравнений")
        self.sup2 = QLabel()
        self.sup2.setText("Обратная система уравнений")
        self.sup3 = QLabel()
        self.sup3.setText("Значение параметра")
        self.sup4 = QLabel()
        self.sup4.setText("Буква праметра")
        self.sup5 = QLabel()
        self.sup5.setText("Точность:")
        self.sup6 = QLabel()
        self.sup6.setText("Символы:")
        self.sup7 = QLabel()
        self.sup7.setText("Кол-во итераций")
        self.sup8 = QLabel()
        self.sup8.setText("Кол-во итераций построить")
        self.sup9 = QLabel()
        self.sup9.setText("Значение вектора начальной точки:")

        self.button1 = QPushButton("построить график")
        self.button2 = QPushButton("[debug] загрузить данные в прогу")
        #self.button1.clicked.connect(self.postroit1)
        self.button2.clicked.connect(self.debug_read_input)

        self.layout_input.addWidget(self.sup1,0,0)
        self.layout_input.addWidget(self.sup2,0,1)
        self.layout_input.addWidget(self.txt_fun1,1,0)
        self.layout_input.addWidget(self.txt_fun2,2,0)
        self.layout_input.addWidget(self.txt_fun1rev,1,1)
        self.layout_input.addWidget(self.txt_fun2rev,2,1)
        self.layout_input.addWidget(self.sup3,3,0)
        self.layout_input.addWidget(self.sup4,3,1)
        self.layout_input.addWidget(self.txt_parvalue,4,0)
        self.layout_input.addWidget(self.txt_parname,4,1)
        self.layout_input.addWidget(self.sup5,5,0)
        self.layout_input.addWidget(self.txt_accvalue,5,1)
        self.layout_input.addWidget(self.sup6,6,0)
        self.layout_input.addWidget(self.txt_symbols,6,1)
        self.layout_input.addWidget(self.sup7,7,0)
        self.layout_input.addWidget(self.sup8,7,1)
        self.layout_input.addWidget(self.txt_iterc,8,0)
        self.layout_input.addWidget(self.txt_iterp,8,1)
        self.layout_input.addWidget(self.sup9,9,0)
        self.layout_input.addWidget(self.txt_start,9,1)
        
        self.layout_input.addWidget(self.button2,10,0)
        self.layout_input.addWidget(self.button1,10,1)

        
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
        self.str_fun1 = self.txt_fun1.text()
        self.str_fun2 = self.txt_fun2.text()
        self.str_fun1rev = self.txt_fun1rev.text()
        self.str_fun2rev = self.txt_fun2rev.text()
        self.str_accvalue = self.txt_accvalue.text()
        self.str_iterc = self.txt_iterc.text()
        self.str_iterp = self.txt_iterp.text()
        
        self.str_start = eval(self.txt_start.text())
        self.symbols = []
        for ii,elem in enumerate(self.txt_symbols.text().split(",")):
            self.symbols.append(elem)
        print(self.symbols, self.str_start)
        
        df1_dx = diff(self.str_fun1, self.symbols[0])
        df1_dy = diff(self.str_fun1,  self.symbols[1])
        df2_dx = diff(self.str_fun2,  self.symbols[0])
        df2_dy = diff(self.str_fun2,  self.symbols[1])
        self.Df_const = [[df1_dx,df1_dy],[df2_dx,df2_dy]]
        print(self.Df_const)
        
        self.str_parvalue = self.txt_parvalue.text()
        self.str_parname = self.txt_parname.text()
        print(self.str_parvalue, self.str_parname)
        
        Df = self.Df_const
        for i, ilist in enumerate(Df):
            for ii,iielem in enumerate(ilist):
                for iii,symb in enumerate(self.symbols):
                    Df[i][ii] = str(Df[i][ii]).replace(symb, enc(self.str_start[iii]))
                Df[i][ii] = eval(Df[i][ii].replace(self.str_parname, enc(self.str_parvalue)))
                print(Df[i][ii])
        
        print(Df)





app = QApplication([])
window = MainWindow()
window.show()
app.exec()

"""
def string_to_lambda(s):
    return eval(s)

# Test
s = 'lambda x: x + 2'
f = string_to_lambda(s)
print(f(5))


 
"""