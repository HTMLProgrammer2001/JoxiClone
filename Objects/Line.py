from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import QPoint
from math import sqrt

from Objects.IObject import IObject
from Context.ObjectData.LineContext import LineContext
from Context.DrawData.LineDrawContext import LineDrawContext


class Line(IObject):
    def __init__(self, context: LineContext):
        self.context = context

    def draw(self, image):
        qp = QPainter(image)
        qp.setPen(QPen(self.context.draw.stroke, self.context.draw.width))
        qp.drawLine(self.context.begin, self.context.end)

    def contain(self, point: QPoint) -> bool:
        begin = self.context.begin
        end = self.context.end

        distance = lambda point, point2: sqrt((point.x() - point2.x())**2 + (point.y() - point2.y())**2)
        lineContain = lambda point: abs(distance(begin, point) + distance(end, point) - \
                                        distance(begin, end)) < self.context.draw.width

        return lineContain(point)

    def getPos(self) -> QPoint:
        return QPoint(self.context.begin.x(), self.context.begin.y())

    def moveTo(self, pos: QPoint):
        beginPoint = self.context.begin
        endPoint = self.context.end

        newEnd = QPoint(endPoint.x() + (pos.x() - beginPoint.x()), endPoint.y() + (pos.y() - beginPoint.y()))

        self.context.setBegin(pos)
        self.context.setEnd(newEnd)

    def moveBy(self, dx: int, dy: int):
        beginPoint = self.context.begin
        endPoint = self.context.end

        beginPoint.setX(beginPoint.x() + dx)
        beginPoint.setY(beginPoint.y() + dy)

        self.context.setBegin(beginPoint)

        endPoint.setX(endPoint.x() + dx)
        endPoint.setY(endPoint.y() + dy)

        self.context.setEnd(endPoint)

    def changeDraw(self, drawContext: LineDrawContext):
        self.context.setDraw(drawContext)
