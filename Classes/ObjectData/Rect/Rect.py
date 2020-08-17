from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import QPoint, QRect

from Classes.ObjectData.Rect.RectDrawContext import RectDrawContext
from Classes.ObjectData.Rect.RectMemento import RectMemento
from Intefaces.IObject import IObject
from Classes.States.Edit.EditRectState import EditRectState
from Intefaces.IEditState import IEditState
from Common.helpers import rectContain


class Rect(IObject):
    rect: QRect = None

    def __init__(self, rect: QRect, drawContext: RectDrawContext):
        self.setDrawContext(drawContext)
        self.setRect(rect)

    def draw(self, image):
        qp = QPainter(image)

        qp.fillRect(self.rect, self.drawContext.fill)
        qp.setPen(QPen(self.drawContext.stroke, self.drawContext.width))
        qp.drawRect(self.rect)

    def contain(self, point: QPoint) -> bool:
        return rectContain(point, self.rect)

    def getPos(self) -> QPoint:
        pos = self.rect.topLeft()

        return QPoint(pos.x(), pos.y())

    def moveTo(self, pos: QPoint):
        self.rect.moveTo(pos)

    def moveBy(self, dx: int, dy: int):
        topLeft = self.rect.topLeft()
        newPoint = QPoint(topLeft.x() + dx, topLeft.y() + dy)

        self.rect.moveTopLeft(newPoint)

    def getEditMode(self, app) -> IEditState:
        return EditRectState(app, self)

    def setRect(self, rect: QRect):
        self.rect = rect

    def getRect(self) -> QRect:
        return self.rect

    def getMemento(self) -> RectMemento:
        return RectMemento(self, self.getRect(), self.getDrawContext())
