from copy import copy
from typing import List

from PyQt5.QtGui import QPainter, QPen, QPolygon, QColor
from PyQt5.QtCore import QPoint, Qt

from Classes.ObjectData.Pen.PenMemento import PenMemento
from Classes.States.Edit.EditPenState import EditPenState
from Intefaces.IEditState import IEditState
from Intefaces.IObject import IObject


class Pen(IObject):
    points: List[QPoint] = None

    def __init__(self, points: List[QPoint], drawContext):
        self.setPoints(points)
        self.setDrawContext(drawContext)

    def draw(self, image):
        qp = QPainter(image)

        qp.setPen(QPen(self.drawContext.stroke, self.drawContext.width))
        qp.drawPolyline(QPolygon(self.points))

        qp.setPen(QPen(Qt.transparent, 0))
        qp.setBrush(self.drawContext.fill)
        qp.drawPolygon(QPolygon(self.points))

    def contain(self, point: QPoint) -> bool:
        return QPolygon(self.getPoints()).containsPoint(point, Qt.OddEvenFill)

    def getPos(self) -> QPoint:
        return self.points[0]

    def moveTo(self, pos: QPoint):
        pass

    def moveBy(self, dx: int, dy: int):
        for point in self.points:
            point.setX(point.x() + dx)
            point.setY(point.y() + dy)

    def getEditMode(self, app) -> IEditState:
        return EditPenState(app, self)

    def getPoints(self) -> List[QPoint]:
        return copy(self.points)

    def setPoints(self, points: List[QPoint]):
        self.points = points

    def getMemento(self) -> PenMemento:
        return PenMemento(self, self.getPoints(), self.getDrawContext())
