from PyQt5.QtGui import QPainter
from PyQt5.QtCore import QPoint

from Objects.IObject import IObject
from Context.ObjectData.EllipseContext import EllipseContext


class Ellipse(IObject):
    def __init__(self, context: EllipseContext):
        self.context = context

    def draw(self, image):
        qp = QPainter(image)

        qp.setBrush(self.context.draw.fill)
        qp.drawEllipse(self.context.center, self.context.radiusX, self.context.radiusY)

    def contain(self, point: QPoint) -> bool:
        distance = ((point.x() - self.context.center.x())/self.context.radiusX)**2 + \
                   ((point.y() - self.context.center.y())/self.context.radiusY)

        return distance <= 1

    def getPos(self) -> QPoint:
        return QPoint(self.context.center.x(), self.context.center.y())

    def moveTo(self, pos: QPoint):
        self.context.center = pos

    def moveBy(self, dx: int, dy: int):
        point = self.context.center

        point.setX(point.x() + dx)
        point.setY(point.y() + dy)

        self.context.center = point
