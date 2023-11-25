import sys
import numpy as np
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget)
from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import axes3d

class ApplicationWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        # Central widget
        self._main = QWidget()
        self.setCentralWidget(self._main)
        # Figure
        self.fig = Figure(figsize=(5, 3))
        self.canvas = FigureCanvas(self.fig)
        # Layout
        layout = QVBoxLayout(self._main)
        layout.addWidget(self.canvas)
        # 3D plot
        self._ax = self.canvas.figure.add_subplot(projection="3d")
        self.X, self.Y, self.Z = axes3d.get_test_data(0.03)
        self._ax.plot_wireframe(self.X, self.Y, self.Z, rstride=10, cstride=10, cmap="viridis")
        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = ApplicationWindow()
    w.show()
    sys.exit(app.exec())
