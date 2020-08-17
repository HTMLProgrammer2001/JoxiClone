from copy import copy

from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import QPoint

from Classes.ObjectData.Ellipse.EllipseDrawContext import EllipseDrawContext
from Classes.ObjectData.Ellipse.EllipseMemento import EllipseMemento
from Intefaces.IObject import IObject
from Intefaces.IEditState import IEditState
from Classes.States.Edit.EditEllipseState import EditEllipseState
from Common.helpers import getEllipseDistance


class Ellipse(IObject):
    def __init__(self, center: QPoint, radX: int, radY: int, drawContext: EllipseDrawContext):
        self.drawContext = drawContext
        self.center = center
        self.radiusX = radX
        self.radiusY = radY

    def draw(self, image):
        qp = QPainter(image)

        qp.setBrush(self.drawContext.fill)
        qp.setPen(QPen(self.drawContext.stroke, self.drawContext.width))
        qp.drawEllipse(self.center, self.radiusX, self.radiusY)

    def contain(self, point: QPoint) -> bool:
        distance = getEllipseDistance(point, self.center, self.radiusX, self.radiusY)
        return distance <= 1

    def getPos(self) -> QPoint:
        return QPoint(self.center.x(), self.center.y())

    def moveTo(self, pos: QPoint):
        self.setCenter(pos)

    def moveBy(self, dx: int, dy: int):
        point = self.getCenter()

        point.setX(point.x() + dx)
        point.setY(point.y() + dy)

        self.setCenter(point)

    def getEditMode(self, app) -> IEditState:
        return EditEllipseState(app, self)

    def getMemento(self):
        return EllipseMemento(self, self.getCenter(), self.getRadiusX(),
                              self.getRadiusY(), self.getDrawContext())

    def setCenter(self, pos: QPoint):
        self.center = pos

    def getCenter(self):
        return copy(self.center)

    def setRadiusX(self, rad: int):
        self.radiusX = rad

    def setRadiusY(self, rad: int):
        self.radiusY = rad

    def getRadiusX(self) -> int:
        return self.radiusX

    def getRadiusY(self) -> int:
        return self.radiusY
