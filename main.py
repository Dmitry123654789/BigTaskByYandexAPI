import os
import sys
from math import cos, radians

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow

from ui_file import Ui_MainWindow
from utilits import get_response_map, get_json


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.map_ll = [37.617698, 55.755864]
        self.z = 18
        self.theme = 'light'
        self.points = set()
        self.adress = 'Россия, Москва'
        self.post_index = 'отсутствует'
        self.set_connect_function()
        self.show_text_adress()
        self.draw_map()

    def set_connect_function(self):
        self.radioButton_dark.clicked.connect(self.set_dark)
        self.radioButton_light.clicked.connect(self.set_light)
        self.pushButton_searh.clicked.connect(self.searh)
        self.pushButton_del_point.clicked.connect(self.del_searh_obj)
        self.checkBox_postIndex.checkStateChanged.connect(self.show_text_adress)

    def click_map(self, x, y):
        x, y = x - self.label_map.pos().x(), y - self.label_map.pos().y()
        if all([self.label_map.width() >= x >= 0, self.label_map.height() >= y >= 0]):
            coord_to_geo_x, coord_to_geo_y = 0.0000428, 0.0000428
            y = self.label_map.height() // 2 - y
            x = x - self.label_map.width() // 2

            ly = (float(self.map_ll[0]) + x * coord_to_geo_x * 2 ** (15 - self.z))
            lx = float(self.map_ll[1]) + y * coord_to_geo_y * cos(radians(float(self.map_ll[1]))) * 2 ** (15 - self.z)
            if ly > 180:
                ly -= 360
            elif ly < -180:
                ly += 360


            if not (lx > 90 or lx < -90):
                self.lineEdit_searh.setText(f'{ly},{lx}')
                self.searh(coord=f'{ly},{lx}')
                self.draw_map()
                self.lineEdit_searh.setText('')

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self.click_map(e.pos().x(), e.pos().y())

    def show_text_adress(self):
        if self.checkBox_postIndex.isChecked():
            self.label_adress.setText('Адрес: ' + self.adress + '\nПочтовый индекс: ' + self.post_index)
        else:
            self.label_adress.setText('Адрес: ' + self.adress)

    def del_searh_obj(self):
        answer = get_json(self.lineEdit_searh.text())
        if answer:
            result = ','.join(map(str, self.map_ll))
            if result in self.points:
                self.points.remove(result)
                self.draw_map()
            self.post_index = self.adress = ''
        self.show_text_adress()

    def searh(self, coord=None):
        answer = get_json(self.lineEdit_searh.text())
        if answer:
            if coord  is None:
                self.map_ll = list(map(float, answer['Point']['pos'].split()))
                self.points.add(','.join(map(str, self.map_ll)))
            else:
                self.points.add(coord)
            self.adress = answer['metaDataProperty']['GeocoderMetaData']['AddressDetails']['Country']['AddressLine']
            adress = answer["metaDataProperty"]["GeocoderMetaData"]["Address"]
            if 'postal_code' in adress:
                self.post_index = str(adress['postal_code'])
            else:
                self.post_index = 'отсутствует'
            self.draw_map()
        else:
            self.adress = 'ничего не найдено'
            self.post_index = 'отсутствует'
        self.show_text_adress()

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
