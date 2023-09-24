from PySide6.QtWidgets import QApplication, QGroupBox, QVBoxLayout, QPushButton, QWidget

def create_group_box():
    group_box = QGroupBox("Group Box")

    layout = QVBoxLayout()
    layout.addWidget(QPushButton("Button 1"))
    layout.addWidget(QPushButton("Button 2"))
    layout.addWidget(QPushButton("Button 3"))

    group_box.setLayout(layout)

    return group_box

app = QApplication([])

window = QWidget()
layout = QVBoxLayout(window)
layout.addWidget(create_group_box())

window.show()

app.exec()