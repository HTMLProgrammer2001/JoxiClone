from PyQt5.QtCore import QPoint

from Context.DrawData.EllipseDrawContext import EllipseDrawContext


class EllipseContext:
    def __init__(self, center: QPoint, radiusX: int = 0, radiusY: int = 0, draw: EllipseDrawContext = None):
        self.center = center
        self.radiusX = radiusX
        self.radiusY = radiusY
        self.draw = draw

    def setCenter(self, center: QPoint):
        self.center = center

    def setRadiusX(self, radius: int):
        self.radiusX = radius

    def setRadiusY(self, radius: int):
        self.radiusY = radius

    def setDraw(self, newDraw: EllipseDrawContext):
        self.draw = newDraw
