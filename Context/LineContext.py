from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPen


class LineContext:
    def __init__(self, begin: QPoint, end: QPoint, pen: QPen = None):
        self.begin = begin
        self.end = end
        self.pen = pen

    def setBegin(self, begin: QPoint):
        self.begin = begin

    def setEnd(self, end: QPoint):
        self.end = end

    def setPen(self, pen: QPen):
        self.pen = pen
