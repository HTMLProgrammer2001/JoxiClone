from PyQt5.QtGui import QPainter
from PyQt5.QtCore import QPoint

from Objects.IObject import IObject
from Context.ObjectData.CircleContext import CircleContext


class Circle(IObject):
    def __init__(self, context: CircleContext):
        self.context = context

    def draw(self, image):
        qp = QPainter(image)
        qp.setPen(self.context.pen)
        qp.drawEllipse(self.context.center, self.context.radius, self.context.radius)

    def contain(self, point: QPoint) -> bool:
        distance = (point.x() - self.context.center.x()) ** 2 + (point.y() - self.context.center.y()) ** 2
        return distance < self.context.radius ** 2

    def getPos(self) -> QPoint:
        return QPoint(self.context.center.x(), self.context.center.y())

    def moveTo(self, pos: QPoint):
        self.context.center = pos

    def moveBy(self, dx: int, dy: int):
        point = self.context.center

        point.setX(point.x() + dx)
        point.setY(point.y() + dy)

        self.context.center = point
