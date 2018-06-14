from PyQt5.QtWidgets import QWidget, QMainWindow
from PyQt5.QtGui import QPainter, QPen, QBrush
from PyQt5.QtCore import Qt


class Painting(QWidget):
    def __init__(self, res, cell):
        super().__init__()
        self.cell = cell
        self.margin = 15
        self.res = res
        self.setGeometry(self.margin, self.margin,
                         self.cell*(self.res[0]['a']) + 2 * self.margin,
                         self.cell*(self.res[0]['b']) + 2 * self.margin)
        self.setWindowTitle('Guillotine cuts map')

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawLines(qp)
        qp.end()

    def drawLines(self, qp):
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        qp.setPen(pen)
        i = 0
        for item in self.res:
            if i == 0:
                qp.drawLine(self.margin, self.margin, self.margin + item['a'] * self.cell, self.margin)
                qp.drawLine(self.margin, self.margin + item['b'] * self.cell,
                            self.margin + item['a'] * self.cell, self.margin + item['b'] * self.cell)
                qp.drawLine(self.margin, self.margin, self.margin, self.margin + item['b'] * self.cell)
                qp.drawLine(self.margin + item['a'] * self.cell, self.margin,
                            self.margin + item['a'] * self.cell, self.margin + item['b'] * self.cell)
                qp.drawText(0, 0,
                            self.margin * 2 + item['a'] * self.cell,
                            self.margin * 2 + item['b'] * self.cell,
                            Qt.AlignHCenter, str(item['a']) + 'x' + str(item['b']))
                i += 1
            if item.get('cut') == 1:
                qp.drawLine(self.margin + (item['x'] + item['m']) * self.cell, self.margin + item['y'] * self.cell,
                            self.margin + (item['x'] + item['m']) * self.cell,
                            self.margin + (item['y'] + item['b']) * self.cell)
            elif item.get('cut') == 0:
                qp.drawLine(self.margin + item['x'] * self.cell, self.margin + (item['y'] + item['m']) * self.cell,
                            self.margin + (item['x'] + item['a']) * self.cell,
                            self.margin + (item['y'] + item['m']) * self.cell)
            elif item.get('cut') is None:
                qp.drawText(self.margin + item['x'] * self.cell,
                            self.margin + item['y'] * self.cell,
                            item['a'] * self.cell,
                            item['b'] * self.cell,
                            Qt.AlignCenter, str(item['a']) + 'x' + str(item['b']))
            if item.get('det') == 'n':
                brush = QBrush(Qt.BDiagPattern)
                qp.setBrush(brush)
                qp.drawRect(self.margin + item['x'] * self.cell,
                            self.margin + item['y'] * self.cell,
                            item['a'] * self.cell,
                            item['b'] * self.cell)
