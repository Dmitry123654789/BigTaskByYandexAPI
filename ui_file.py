# Form implementation generated from reading ui file 'wind.ui'
#
# Created by: PyQt6 UI code generator 6.8.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(31, -1, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit_searh = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.lineEdit_searh.setObjectName("lineEdit_searh")
        self.horizontalLayout.addWidget(self.lineEdit_searh)
        self.pushButton_searh = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton_searh.setObjectName("pushButton_searh")
        self.horizontalLayout.addWidget(self.pushButton_searh)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(-1, 0, -1, 0)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.radioButton_light = QtWidgets.QRadioButton(parent=self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.radioButton_light.setFont(font)
        self.radioButton_light.setChecked(True)
        self.radioButton_light.setObjectName("radioButton_light")
        self.verticalLayout.addWidget(self.radioButton_light)
        self.radioButton_dark = QtWidgets.QRadioButton(parent=self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.radioButton_dark.setFont(font)
        self.radioButton_dark.setObjectName("radioButton_dark")
        self.verticalLayout.addWidget(self.radioButton_dark)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.label_map = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_map.setText("")
        self.label_map.setObjectName("label_map")
        self.verticalLayout_2.addWidget(self.label_map)
        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.setStretch(1, 9)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_searh.setText(_translate("MainWindow", "Искать"))
        self.radioButton_light.setText(_translate("MainWindow", "Светлая"))
        self.radioButton_dark.setText(_translate("MainWindow", "Темная"))
