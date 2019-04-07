# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(220, 40, 341, 161))
        font = QtGui.QFont()
        font.setFamily("Old English Text MT")
        font.setPointSize(21)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.pushButton_Start = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Start.setGeometry(QtCore.QRect(50, 350, 201, 81))
        self.pushButton_Start.setObjectName("pushButton_Start")
        self.pushButton_About = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_About.setGeometry(QtCore.QRect(300, 370, 201, 81))
        self.pushButton_About.setObjectName("pushButton_About")
        self.pushButton_Exit = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Exit.setGeometry(QtCore.QRect(560, 390, 201, 81))
        self.pushButton_Exit.setObjectName("pushButton_Exit")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.pushButton_Exit.clicked.connect(MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "OptionPayOffer"))
        self.label.setText(_translate("MainWindow", "Welcome to OptionPayOffer!"))
        self.pushButton_Start.setText(_translate("MainWindow", "Start"))
        self.pushButton_About.setText(_translate("MainWindow", "About"))
        self.pushButton_Exit.setText(_translate("MainWindow", "Exit"))


