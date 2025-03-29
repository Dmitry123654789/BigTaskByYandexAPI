import os
import sys
from math import cos, radians

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow

from ui_file import Ui_MainWindow
from utilits import get_response_map, get_json, get_organisation_json, lonlat_distance


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

    def found_coord(self, x, y):
        coord_to_geo_x, coord_to_geo_y = 0.0000428, 0.0000428  # Отношение пиксельной сетки к геогорафической сетке
        y = self.label_map.height() // 2 - y
        x = x - self.label_map.width() // 2

        ly = (float(self.map_ll[0]) + x * coord_to_geo_x * 2 ** (15 - self.z))
        lx = float(self.map_ll[1]) + y * coord_to_geo_y * cos(radians(float(self.map_ll[1]))) * 2 ** (15 - self.z)
        if ly > 180:
            ly -= 360
        elif ly < -180:
            ly += 360
        return lx, ly

    def click_map_left(self, x, y):
        x, y = x - self.label_map.pos().x(), y - self.label_map.pos().y()
        if all([self.label_map.width() >= x >= 0, self.label_map.height() >= y >= 0]):
            lx, ly = self.found_coord(x, y)
            if not (lx > 90 or lx < -90):
                self.lineEdit_searh.setText(f'{ly},{lx}')
                self.searh(coord=[ly, lx], color_pt='pm2rdm')
                self.lineEdit_searh.setText('')
            else:
                self.points = set()
        self.draw_map()

    def click_map_right(self, x, y):
        x, y = x - self.label_map.pos().x(), y - self.label_map.pos().y()
        if all([self.label_map.width() >= x >= 0, self.label_map.height() >= y >= 0]):
            lx, ly = self.found_coord(x, y)
            if not (lx > 90 or lx < -90):
                new_point = [50, None, '']

                for orzaniz in open('organization.txt', encoding='utf-8').readlines():
                    for place in get_organisation_json(f'{ly},{lx}', orzaniz.strip()):
                        coord_organization = place["geometry"]["coordinates"]
                        # print(orzaniz.strip(), lonlat_distance(coord_organization, (ly, lx)))
                        if lonlat_distance(coord_organization, (ly, lx)) <= new_point[0]:
                            print('dsdsdsdsdsdsdsdsdsdsdsdsdsdsdsd')
                            new_point = [lonlat_distance(coord_organization, (ly, lx)), place['properties']['description'], coord_organization]
                print(new_point)
                if not new_point[1] is None:
                    print('yes')
                    self.lineEdit_searh.setText(new_point[1])
                    self.searh(coord=new_point[2], color_pt='pm2am')
                    self.lineEdit_searh.setText('')
                else:
                    self.del_info_organization()
            else:
                self.del_info_organization()


        self.show_text_adress()
        self.draw_map()

    def del_info_organization(self):
        self.points = set()
        self.adress = f'Нет организаций в радиусе 50 метров'
        self.post_index = ''


    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self.click_map_left(e.pos().x(), e.pos().y())
        elif e.button() == Qt.MouseButton.RightButton:
            self.click_map_right(e.pos().x(), e.pos().y())

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
        self.points = set()
        self.lineEdit_searh.setText('')
        self.show_text_adress()
        self.draw_map()

    def searh(self, coord=None, color_pt=''):
        answer = get_json(self.lineEdit_searh.text())
        if answer:
            self.points = set()
            formate_coord = list(map(float, answer['Point']['pos'].split()))
            if coord is None or type(coord) is bool:
                self.map_ll = formate_coord
            else:
                formate_coord = coord
            if color_pt != '':
                self.points.add(','.join(map(str, formate_coord)) + ',' + color_pt)
            else:
                self.points.add(','.join(map(str, formate_coord)))

            try:
                self.adress = answer['metaDataProperty']['GeocoderMetaData']['AddressDetails']['Country']['AddressLine']
            except KeyError:
                self.adress = answer['metaDataProperty']['GeocoderMetaData']['AddressDetails']["Address"]
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
