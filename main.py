import os
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow

from ui_file import Ui_MainWindow
from utilits import get_response_map, get_point




class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.map_ll = [37.530898, 55.702892]
        self.z = 5
        self.theme = 'light'
        self.points = set()
        self.draw_map()
        self.radioButton_dark.clicked.connect(self.set_dark)
        self.radioButton_light.clicked.connect(self.set_light)
        self.pushButton_searh.clicked.connect(self.searh)
        self.pushButton_del_point.clicked.connect(self.del_searh_obj)

    def del_searh_obj(self):
        self.label_adress.setText('Адрес:')
        answer = get_point(self.lineEdit_searh.text())
        if answer:
            result = ','.join(map(str, self.map_ll))
            if result in self.points:
                self.points.remove(result)
                self.draw_map()


    def searh(self):
        answer = get_point(self.lineEdit_searh.text())
        if answer:
            self.map_ll = list(map(float, answer['Point']['pos'].split()))
            self.points.add(','.join(map(str, self.map_ll)))
            self.label_adress.setText(
                'Адрес: ' + answer['metaDataProperty']['GeocoderMetaData']['AddressDetails']['Country']['AddressLine'])
            self.draw_map()

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
        if event.key() == Qt.Key.Key_Return:
            self.searh()
        else:
            self.draw_map()

    def draw_map(self):
        response = get_response_map(','.join(map(str, self.map_ll)), self.z, self.theme, self.points)
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
