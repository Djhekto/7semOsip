
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QStackedLayout,QLineEdit, QGridLayout, QLabel,QTableWidget, QTableWidgetItem
from PySide6.QtGui import QAction, QColor , QPainter, QPixmap
from PySide6.QtCore import Qt
import pyqtgraph as pg


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("prog -997")
        self.layout_stack = QStackedLayout()

#--------------------------------------------------------------------------
        self.layout_input = QGridLayout()

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
        
        self.W_HIGHT = 700
        self.W_WIDTH = 700
		
        self.picture_out1 = QLabel()
        self.picture_out1.setMinimumSize(self.W_WIDTH, self.W_HIGHT)
        self.layout_graph.addWidget( self.picture_out1)
        
        pixmap = QPixmap(self.W_HIGHT, self.W_WIDTH)
        pixmap.fill(Qt.white)

        painter = QPainter(pixmap)
        painter.setPen(QColor(255, 0, 0))#
        painter.setBrush(QColor(255, 0, 0))
        
        painter.drawRect(int(self.W_WIDTH/2), 0, 0, self.W_HIGHT) #VERTICAL
        painter.drawRect(0, int(self.W_HIGHT/2), self.W_WIDTH, 0) #HORISONTAL
        
        painter.end()
        self.picture_out1.setPixmap(pixmap)

        self.widget_graph = QWidget()
        self.widget_graph.setLayout(self.layout_graph)
        self.layout_stack.addWidget(self.widget_graph)

#--------------------------------------------------------------------------
        self.layout_out = QGridLayout()

        self.res_out1 = QLabel()
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

app = QApplication([])
window = MainWindow()
window.show()
app.exec()
