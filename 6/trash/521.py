import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.axis = self.figure.add_subplot(111, projection='3d')

        _layout = QVBoxLayout()
        _layout.addWidget(self.canvas)
        _widget = QWidget()
        _widget.setLayout(_layout)
        self.setCentralWidget(_widget)

        self.draw_3d_bar()

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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())
