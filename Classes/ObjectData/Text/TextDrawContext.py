from PyQt5.QtGui import QFont, QColor

from Intefaces.IContext import IContext


class TextDrawContext(IContext):
    def __init__(self, font: QFont, stroke: QColor):
        self.font = font
        self.stroke = stroke

    def setFont(self, font: QFont):
        self.font = font

    def setStroke(self, newStroke: QColor):
        self.stroke = newStroke
