from PyQt5.QtGui import QPainter
from PyQt5.QtCore import QPoint

from Objects.IObject import IObject
from Context.LineContext import LineContext


class Line(IObject):
    def __init__(self, context: LineContext):
        self.context = context

    def draw(self, image):
        qp = QPainter(image)
        qp.setPen(self.context.pen)
        qp.drawLine(self.context.begin, self.context.end)

    def contain(self, point: QPoint) -> bool:
        begin = self.context.begin
        end = self.context.end

        lineForm = lambda x: (x - begin.x()) * (end.y() - begin.y()) / (end.x() - begin.x()) + begin.y()

        return abs(lineForm(point.x()) - point.y()) < self.context.pen.width()

    def moveTo(self, pos: QPoint):
        pass

    def moveBy(self, dx: int, dy: int):
        beginPoint = self.context.begin
        endPoint = self.context.end

        beginPoint.setX(beginPoint.x() + dx)
        beginPoint.setY(beginPoint.y() + dy)

        self.context.begin = beginPoint

        endPoint.setX(endPoint.x() + dx)
        endPoint.setY(endPoint.y() + dy)

        self.context.end = endPoint
