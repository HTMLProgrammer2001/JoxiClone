from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import QPoint, QRect

from Context.RectDrawContext import RectDrawContext
from Memento.RectMemento import RectMemento
from Objects.IObject import IObject
from States.Edit.EditRectState import EditRectState
from States.Edit.IEditState import IEditState
from helpers import rectContain


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
