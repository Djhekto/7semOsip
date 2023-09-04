from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QStackedLayout,QLineEdit, QGridLayout, QLabel,QTableWidget, QTableWidgetItem
from PySide6.QtGui import QAction, QColor
import pyqtgraph as pg


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
        self.txt_parvalue = QLineEdit( "1,35" )
        self.txt_parname = QLineEdit( "a" )
        self.txt_accvalue = QLineEdit( "0.1" )
        self.txt_symbols = QLineEdit( "x,y" )
        self.txt_iterc = QLineEdit( "1000" )
        self.txt_iterp = QLineEdit( "1000" )
        self.txt_start = QLineEdit( "0,0")

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
        #self.button1.clicked.connect(self.postroit1)

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
        
        self.layout_input.addWidget(self.button1,10,0)

        
        self.widget_input = QWidget()
        self.widget_input.setLayout(self.layout_input)
        self.layout_stack.addWidget(self.widget_input)
        
#--------------------------------------------------------------------------
        self.layout_graph = QVBoxLayout()
        
        custom_colour = QColor(240,240,255)
        pg_colour1 = pg.mkColor(custom_colour)
		
        self.plot1 = pg.PlotWidget()
        self.plot1.plot([1, 2, 3, 4, 5], [30, 32, 34, 32, 33])
        self.plot1.setBackground(pg_colour1)
        self.layout_graph.addWidget(self.plot1)
        
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

app = QApplication([])
window = MainWindow()
window.show()
app.exec_()

"""
def string_to_lambda(s):
    return eval(s)

# Test
s = 'lambda x: x + 2'
f = string_to_lambda(s)
print(f(5))


 
"""