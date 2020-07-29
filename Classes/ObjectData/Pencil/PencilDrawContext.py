from PyQt5.QtGui import QColor

from Intefaces.IContext import IContext


class PencilDrawContext(IContext):
    def __init__(self, stroke: QColor = QColor('red'), width: int = 5):
        self.stroke = stroke
        self.width = width

    def setStroke(self, newStroke: QColor):
        self.stroke = newStroke

    def setWidth(self, newWidth: int):
        self.width = newWidth
