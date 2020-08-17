from copy import copy

from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import QPoint

from Classes.ObjectData.Line.LineMemento import LineMemento
from Intefaces.IObject import IObject
from Classes.ObjectData.Line.LineDrawContext import LineDrawContext
from Classes.States.Edit.EditLineState import EditLineState
from Intefaces.IEditState import IEditState
from Common.helpers import lineContain


class Line(IObject):
    begin: QPoint = None
    end: QPoint = None

    def __init__(self, begin: QPoint, end: QPoint, drawContext: LineDrawContext):
        self.setBegin(begin)
        self.setEnd(end)
        self.setDrawContext(drawContext)

    def draw(self, image):
        qp = QPainter(image)
        qp.setPen(QPen(self.drawContext.stroke, self.drawContext.width))
        qp.drawLine(self.getBegin(), self.getEnd())

    def contain(self, point: QPoint) -> bool:
        return lineContain(point, self.getBegin(), self.getEnd(), self.drawContext.width)

    def getPos(self) -> QPoint:
        return QPoint(self.begin.x(), self.begin.y())

    def moveTo(self, pos: QPoint):
        beginPoint = self.getBegin()
        endPoint = self.getEnd()

        newEnd = QPoint(endPoint.x() + (pos.x() - beginPoint.x()), endPoint.y() + (pos.y() - beginPoint.y()))

        self.setBegin(pos)
        self.setEnd(newEnd)

    def moveBy(self, dx: int, dy: int):
        beginPoint = self.getBegin()
        endPoint = self.getEnd()

        beginPoint.setX(beginPoint.x() + dx)
        beginPoint.setY(beginPoint.y() + dy)

        self.setBegin(beginPoint)

        endPoint.setX(endPoint.x() + dx)
        endPoint.setY(endPoint.y() + dy)

        self.setEnd(endPoint)

    def getEditMode(self, app) -> IEditState:
        return EditLineState(app, self)

    def getBegin(self):
        return copy(self.begin)

    def getEnd(self):
        return copy(self.end)

    def setBegin(self, begin: QPoint):
        self.begin = begin

    def setEnd(self, end: QPoint):
        self.end = end

    def getMemento(self) -> LineMemento:
        return LineMemento(self, self.getBegin(), self.getEnd(), self.getDrawContext())
