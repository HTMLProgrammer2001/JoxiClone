from PyQt5.QtCore import QRect
from PyQt5.QtGui import QPen


class RectContext:
    def __init__(self, rect: QRect, pen: QPen = None, fill: bool = False):
        self.rect = rect
        self.pen = pen
        self.fill = fill

    def setRect(self, rect: QRect):
        self.rect = rect

    def setPen(self, pen: QPen):
        self.pen = pen

    def setFill(self, fill: bool):
        self.fill = fill
