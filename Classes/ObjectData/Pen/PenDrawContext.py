from PyQt5.QtGui import QColor

from Intefaces.IContext import IContext


class PenDrawContext(IContext):
    def __init__(self, fill: QColor = QColor('red'), stroke: QColor = QColor('red'), width: int = 5):
        self.stroke = stroke
        self.width = width
        self.fill = fill

    def setStroke(self, newStroke: QColor):
        self.stroke = newStroke

    def setWidth(self, newWidth: int):
        self.width = newWidth

    def setFill(self, newFill: QColor):
        self.fill = newFill
