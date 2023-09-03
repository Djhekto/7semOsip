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

        #default input

        self.txt_lineedit = QLineEdit( )
        self.button1 = QPushButton("построить график")
        #self.button1.clicked.connect(self.postroit1)
        self.sup1 = QLabel()
        self.sup1.setText("Система уравнений")
        
        self.layout_input.addWidget(self.sup1,0,0)
        self.layout_input.addWidget(self.txt_lineedit,1,0)
        self.layout_input.addWidget(self.button1,1,1)

        
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