# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'start_window.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QMainWindow


class PaintWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.horizontalLayout_7.addWidget(self.label)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_6.addWidget(self.label_3)
        self.sheetWidth = QtWidgets.QLineEdit(self.centralwidget)
        self.sheetWidth.setObjectName("sheetWidth")
        self.horizontalLayout_6.addWidget(self.sheetWidth)
        self.horizontalLayout_7.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_5.addWidget(self.label_2)
        self.sheetHeight = QtWidgets.QLineEdit(self.centralwidget)
        self.sheetHeight.setObjectName("sheetHeight")
        self.horizontalLayout_5.addWidget(self.sheetHeight)
        self.horizontalLayout_7.addLayout(self.horizontalLayout_5)
        self.verticalLayout_3.addLayout(self.horizontalLayout_7)
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        self.verticalLayout_3.addWidget(self.tableWidget)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_2.addWidget(self.label_6)
        self.detailHeight = QtWidgets.QLineEdit(self.centralwidget)
        self.detailHeight.setObjectName("detailHeight")
        self.horizontalLayout_2.addWidget(self.detailHeight)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.label_4)
        self.detailWidth = QtWidgets.QLineEdit(self.centralwidget)
        self.detailWidth.setObjectName("detailWidth")
        self.horizontalLayout.addWidget(self.detailWidth)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter_2 = QtWidgets.QSplitter(self.centralwidget)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.label_5 = QtWidgets.QLabel(self.splitter_2)
        self.label_5.setObjectName("label_5")
        self.detailCount = QtWidgets.QSpinBox(self.splitter_2)
        self.detailCount.setObjectName("detailCount")
        self.verticalLayout.addWidget(self.splitter_2)
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.verticalLayout.addWidget(self.comboBox)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        self.horizontalLayout_4.addLayout(self.horizontalLayout_3)
        self.addDetail = QtWidgets.QPushButton(self.centralwidget)
        self.addDetail.setObjectName("addDetail")
        self.horizontalLayout_4.addWidget(self.addDetail)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.startButton = QtWidgets.QPushButton(self.centralwidget)
        self.startButton.setObjectName("startButton")
        self.verticalLayout_3.addWidget(self.startButton)
        self.tableWidget.raise_()
        self.addDetail.raise_()
        self.detailCount.raise_()
        self.detailWidth.raise_()
        self.detailHeight.raise_()
        self.label.raise_()
        self.sheetWidth.raise_()
        self.sheetHeight.raise_()
        self.detailHeight.raise_()
        self.startButton.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 479, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

        self.label.setText(_translate("MainWindow", "Main sheet:"))
        self.label_3.setText(_translate("MainWindow", "Width"))
        self.label_2.setText(_translate("MainWindow", "Height"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Count"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Width"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Height"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Needed orientation"))
        self.label_6.setText(_translate("MainWindow", "Height"))
        self.label_4.setText(_translate("MainWindow", "Width "))
        self.label_5.setText(_translate("MainWindow", "Count"))
        self.comboBox.setCurrentText(_translate("MainWindow", "Both orientations"))
        self.comboBox.setItemText(0, _translate("MainWindow", "Both orientations"))
        self.comboBox.setItemText(1, _translate("MainWindow", "Only vertical"))
        self.comboBox.setItemText(2, _translate("MainWindow", "Only horizontal"))
        self.addDetail.setText(_translate("MainWindow", "Add detail"))
        self.startButton.setText(_translate("MainWindow", "Start!"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Paint = QtWidgets.QWidget()
    ui = PaintWindow()
    ui.setupUi(Paint)
    Paint.show()
    sys.exit(app.exec_())

