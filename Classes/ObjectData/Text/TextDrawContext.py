from PyQt5.QtGui import QFont, QColor

from Intefaces.IContext import IContext


class TextDrawContext(IContext):
    def __init__(self, font: QFont, stroke: QColor, size: int, fill: QColor):
        self.font = font
        self.stroke = stroke
        self.width = size
        self.fill = fill

    def setFont(self, font: QFont):
        self.font = font

    def setStroke(self, newStroke: QColor):
        self.stroke = newStroke

    def setFill(self, newFill: QColor):
        self.fill = newFill

    def setWidth(self, newWidth: int):
        self.width = newWidth
