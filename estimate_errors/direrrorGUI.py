# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'direrrorGUI.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(888, 290)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.inputValuesBtn = QtWidgets.QPushButton(self.centralwidget)
        self.inputValuesBtn.setObjectName("inputValuesBtn")
        self.verticalLayout_2.addWidget(self.inputValuesBtn)
        self.appErrorBtn = QtWidgets.QPushButton(self.centralwidget)
        self.appErrorBtn.setObjectName("appErrorBtn")
        self.verticalLayout_2.addWidget(self.appErrorBtn)
        self.measureErrorBtn = QtWidgets.QPushButton(self.centralwidget)
        self.measureErrorBtn.setObjectName("measureErrorBtn")
        self.verticalLayout_2.addWidget(self.measureErrorBtn)
        self.resultBtn = QtWidgets.QPushButton(self.centralwidget)
        self.resultBtn.setObjectName("resultBtn")
        self.verticalLayout_2.addWidget(self.resultBtn)
        self.listClearBtn = QtWidgets.QPushButton(self.centralwidget)
        self.listClearBtn.setObjectName("listClearBtn")
        self.verticalLayout_2.addWidget(self.listClearBtn)
        self.horizontalLayout_4.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
        self.horizontalLayout_4.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 888, 26))
        self.menubar.setObjectName("menubar")
        self.menufile = QtWidgets.QMenu(self.menubar)
        self.menufile.setObjectName("menufile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionHelp = QtWidgets.QAction(MainWindow)
        self.actionHelp.setObjectName("actionHelp")
        self.indirError = QtWidgets.QAction(MainWindow)
        self.indirError.setObjectName("indirError")
        self.menufile.addAction(self.actionOpen)
        self.menufile.addAction(self.actionSave)
        self.menufile.addAction(self.actionHelp)
        self.menubar.addAction(self.menufile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Прямая погрешность"))
        self.inputValuesBtn.setText(_translate("MainWindow", "Измеренные значения"))
        self.appErrorBtn.setText(_translate("MainWindow", "Приборная погрешность"))
        self.measureErrorBtn.setText(_translate("MainWindow", "Погрешность измерения"))
        self.resultBtn.setText(_translate("MainWindow", "Вычислить погрешность"))
        self.listClearBtn.setText(_translate("MainWindow", "Очистить список"))
        self.menufile.setTitle(_translate("MainWindow", "&Файл"))
        self.actionOpen.setText(_translate("MainWindow", "Открыть"))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionSave.setText(_translate("MainWindow", "Сохранить Как..."))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionHelp.setText(_translate("MainWindow", "Помощь"))
        self.actionHelp.setShortcut(_translate("MainWindow", "F1"))
        self.indirError.setText(_translate("MainWindow", "Погрешность косвенных измерений"))

