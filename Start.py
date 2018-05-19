import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget

import AlgorithmClass
from StartWindow import Ui_MainWindow
from MapWindow import MapWindow


class TestDialog(MapWindow):
    def __init__(self, dialog):
        MapWindow.__init__(self)
        self.setupUi(dialog)


class TestApp(Ui_MainWindow):
    def __init__(self, dialog):
        Ui_MainWindow.__init__(self)
        self.setupUi(dialog)

        self.addDetail.clicked.connect(self.addRow)
        self.startButton.clicked.connect(self.startProcess)

    def addRow(self):
        #Retrieve text from QLineEdit
        detailWidth = self.detailWidth.text()
        detailHeight = self.detailHeight.text()
        detailCount = self.detailCount.text()
        comboBox = str(self.comboBox.currentIndex())
        #Create a empty row at bottom of table
        numRows = self.tableWidget.rowCount()
        self.tableWidget.insertRow(numRows)
        #Add text to the row
        self.tableWidget.setItem(numRows, 0, QtWidgets.QTableWidgetItem(detailCount))
        self.tableWidget.setItem(numRows, 1, QtWidgets.QTableWidgetItem(detailWidth))
        self.tableWidget.setItem(numRows, 2, QtWidgets.QTableWidgetItem(detailHeight))
        self.tableWidget.setItem(numRows, 3, QtWidgets.QTableWidgetItem(comboBox))

    def startProcess(self):
        details_square, details_count = 0, 0
        main_sheet = dict()
        details = list()
        main_sheet['a'] = int(self.sheetWidth.text())
        main_sheet['b'] = int(self.sheetHeight.text())
        numRows = self.tableWidget.rowCount()
        for row in range(numRows):
            detailCount = int(self.tableWidget.item(row, 0).text())
            detailWidth = int(self.tableWidget.item(row, 1).text())
            detailHeight = int(self.tableWidget.item(row, 2).text())
            orientation = int(self.tableWidget.item(row, 3).text())
            details.append({
                'sum': detailCount,
                'a': detailWidth if detailWidth >= detailHeight else detailHeight,
                'b': detailHeight if detailWidth >= detailHeight else detailWidth,
                'or': orientation - 1 if 0 < orientation <= 2 else None
            })
            details_square += detailCount * detailWidth * detailHeight
            details_count += detailCount
        first_orient = abs(self.firstOrient.currentIndex() - 1)
        first_cut = abs(self.firstCut.currentIndex() - 1)
        cell = self.unitPx.value()
        algorithm = AlgorithmClass.GuillotineCuts(main_sheet, details, details_square, details_count, first_orient,
                                                  first_cut, cell)
        algorithm.start_process()


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QMainWindow()

    test_1 = TestApp(dialog)

    dialog.show()
    sys.exit(app.exec_())