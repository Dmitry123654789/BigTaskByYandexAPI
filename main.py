import os
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow

from ui_file import Ui_MainWindow
from utilits import get_response_map


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.map_ll = [37.530898, 55.702892]
        self.z = 5
        self.theme = 'light'
        self.draw_map()
        self.radioButton_dark.clicked.connect(self.set_dark)
        self.radioButton_light.clicked.connect(self.set_light)

    def set_dark(self):
        self.theme = 'dark'
        self.draw_map()

    def set_light(self):
        self.theme = 'light'
        self.draw_map()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_PageDown:
            self.z = max(self.z - 1, 0)
        if event.key() == Qt.Key.Key_PageUp:
            self.z = min(self.z + 1, 21)
        if event.key() == Qt.Key.Key_Up:
            self.map_ll[1] += 18 // self.z
        if event.key() == Qt.Key.Key_Down:
            self.map_ll[1] -= 18 // self.z
        if event.key() == Qt.Key.Key_Right:
            self.map_ll[0] += 18 // self.z
        if event.key() == Qt.Key.Key_Left:
            self.map_ll[0] -= 18 // self.z
        self.draw_map()

    def draw_map(self):
        response = get_response_map(','.join(map(str, self.map_ll)), self.z, self.theme)
        if response:
            map_file = "map.png"
            with open(map_file, "wb") as file:
                file.write(response)
            self.label_map.setPixmap(QPixmap(map_file))
            os.remove(map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
