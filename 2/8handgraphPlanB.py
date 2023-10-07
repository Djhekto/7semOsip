
from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PySide6.QtGui import QPainter, QColor, QPixmap
from PySide6.QtCore import Qt

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        W_HIGHT = 700
        W_WIDTH = 700

        self.label = QLabel(self)
        self.label.setMinimumSize(700, 700)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)

        pixmap = QPixmap(W_HIGHT, W_WIDTH)
        pixmap.fill(Qt.white)

        painter = QPainter(pixmap)
        painter.setPen(QColor(255, 0, 0))#
        painter.setBrush(QColor(255, 0, 0))
        
        painter.drawRect(int(W_WIDTH/2), 0, 0, W_HIGHT) #VERTICAL
        painter.drawRect(0, int(W_HIGHT/2), W_WIDTH, 0) #HORISONTAL
        
        painter.setPen(QColor(0, 0, 0))#
        painter.setBrush(QColor(0, 0, 0))
        
        
        painter.drawRect(10, 10, 50, 50)  # Draw first square
        painter.drawRect(70, 70, 50, 50)  # Draw second square
        painter.drawRect(130, 130, 50, 50)  # Draw third square
        painter.end()

        self.label.setPixmap(pixmap)

app = QApplication([])
window = MainWindow()
window.show()
app.exec_()