# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets

from Painting import Painting


class MapWindow(object):
    margin = 10

    def setupUi(self, Dialog, res, cell):
        self.cell = cell
        self.res = res
        Dialog.setObjectName("Dialog")
        Dialog.setGeometry(30, 30,
                         self.cell * (self.res[0]['a']) + 4 * self.margin,
                         self.cell * (self.res[0]['b']) + 4 * self.margin)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Dialog)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget = Painting(res, cell)
        self.widget.setObjectName("widget")
        self.horizontalLayout.addWidget(self.widget)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Guillotine cuts map", "Guillotine cuts map"))
