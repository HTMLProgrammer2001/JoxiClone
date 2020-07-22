from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPen


class CircleContext:
    def __init__(self, center: QPoint = None, radius: int = 0, pen: QPen = None):
        self.center = center
        self.radius = radius
        self.pen = pen

    def setCenter(self, center: QPoint):
        self.center = center

    def setRadius(self, radius: int):
        self.radius = radius

    def setPen(self, pen: QPen):
        self.pen = pen
