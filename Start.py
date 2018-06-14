from PyQt5 import QtCore, QtGui, QtWidgets

import AlgorithmClass
import Algoritm
from PaintWindow import PaintWindow
from StartWindow import Ui_MainWindow


class TestApp2(PaintWindow):
    def __init__(self, dialog):
        PaintWindow.__init__(self)
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
        # details_square, details_count = 0, 0
        # main_sheet = dict()
        # details = list()
        # main_sheet['a'] = int(self.sheetWidth.text())
        # main_sheet['b'] = int(self.sheetHeight.text())
        # numRows = self.tableWidget.rowCount()
        # for row in range(numRows):
        #     detailCount = int(self.tableWidget.item(row, 0).text())
        #     detailWidth = int(self.tableWidget.item(row, 1).text())
        #     detailHeight = int(self.tableWidget.item(row, 2).text())
        #     orientation = int(self.tableWidget.item(row, 3).text())
        #     details.append({
        #         'sum': detailCount,
        #         'a': detailWidth,
        #         'b': detailHeight,
        #         'or': orientation - 1 if orientation > 0 else None
        #     })
        #     details_square += detailCount * detailWidth * detailHeight
        #     details_count += detailCount
        # algorithm = AlgorithmClass.GuillotineCuts(main_sheet, details, details_square, details_count)
        # algorithm.start_process()
        dialog = QtWidgets.QDialog()
        test_1 = TestApp2(dialog)
        dialog.show()
        dialog._exec()


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QMainWindow()

    test_1 = TestApp(dialog)

    dialog.show()
    sys.exit(app.exec_())