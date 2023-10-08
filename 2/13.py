from PySide6.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QGraphicsRectItem
from PySide6.QtCore import Qt, QRectF

def cartesian_to_qrectf(x, y, height):
    # Flip the y-coordinate
    y_qrectf = height - y
    return x, y_qrectf

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Create QGraphicsView and set it as central widget
        self.view = QGraphicsView()
        self.setCentralWidget(self.view)
        
        # Create QGraphicsScene
        self.scene = QGraphicsScene()
        self.view.setScene(self.scene)

        square = QGraphicsRectItem(QRectF(1, 1, 5, 5))  ;        self.scene.addItem(square)
        square = QGraphicsRectItem(QRectF(350, 1, 5, 5))  ;        self.scene.addItem(square)
        square = QGraphicsRectItem(QRectF(1, 350, 5, 5))  ;        self.scene.addItem(square)
        square = QGraphicsRectItem(QRectF(350, 350, 5, 5))  ;        self.scene.addItem(square)


        x_qrectf, y_qrectf = cartesian_to_qrectf(0, 300, 400)
        square = QGraphicsRectItem(QRectF(x_qrectf, y_qrectf, 20, 20)) 
        self.scene.addItem(square)
        
        x_qrectf, y_qrectf = 0, 300
        square = QGraphicsRectItem(QRectF(x_qrectf, y_qrectf, 5, 5)) 
        self.scene.addItem(square)
        
        # Create squares from coordinates and add them to the scene
        # Each coordinate represents the top-left corner of a square
        #coordinates = [(10, 10), (50, 50), (100, 100)]
        ##for x, y in coordinates:
         #   square = QGraphicsRectItem(QRectF(x, y, 20, 20))  # 20x20 square
         #   self.scene.addItem(square)

app = QApplication([])
window = MainWindow()
window.show()
app.exec()