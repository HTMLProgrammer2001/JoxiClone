from PyQt5.QtGui import QColor

from Intefaces.IContext import IContext


class RectDrawContext(IContext):
    def __init__(self, fill: QColor = QColor('red'), stroke: QColor = QColor('red'), width: int = 0):
        self.fill = fill
        self.stroke = stroke
        self.width = width

    def setStroke(self, newStroke: QColor):
        self.stroke = newStroke

    def setFill(self, newFill: QColor):
        self.fill = newFill

    def setWidth(self, newWidth: int):
        self.width = newWidth
