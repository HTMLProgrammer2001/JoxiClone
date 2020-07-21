from PyQt5.QtGui import QPainter
from PyQt5.QtCore import QPoint

from Objects.IObject import IObject
from Context.ObjectData.RectContext import RectContext


class Rect(IObject):
    def __init__(self, context: RectContext):
        self.context = context

    def draw(self, image):
        qp = QPainter(image)

        if self.context.fill:
            qp.fillRect(self.context.rect, self.context.pen.color())
        else:
            qp.drawRect(self.context.rect)

    def contain(self, point: QPoint) -> bool:
        rect = self.context.rect

        return rect.left() < point.x() < rect.right() and rect.top() < point.y() < rect.bottom()

    def getPos(self) -> QPoint:
        pos = self.context.rect.topLeft()
        return QPoint(pos.x(), pos.y())

    def moveTo(self, pos: QPoint):
        self.context.rect.moveTo(pos)

    def moveBy(self, dx: int, dy: int):
        topLeft = self.context.rect.topLeft()
        newPoint = QPoint(topLeft.x() + dx, topLeft.y() + dy)

        self.context.rect.moveTopLeft(newPoint)
