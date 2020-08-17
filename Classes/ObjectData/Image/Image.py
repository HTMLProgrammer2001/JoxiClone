from copy import copy

from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtCore import QPoint, QRect

from Classes.ObjectData.Image.ImageDrawContext import ImageDrawContext
from Classes.ObjectData.Image.ImageMemento import ImageMemento
from Classes.States.Edit.EditImageState import EditImageState
from Intefaces.IEditState import IEditState
from Intefaces.IObject import IObject
from Common.helpers import rectContain


class Image(IObject):
    def __init__(self, path: str, drawContext: ImageDrawContext):
        self.drawContext = drawContext
        self.rect = QPixmap(path).rect()
        self.path = path

    def draw(self, image):
        qp = QPainter(image)
        image = QPixmap(self.path).toImage()

        qp.drawImage(self.rect, image, image.rect())

    def contain(self, point: QPoint) -> bool:
        return rectContain(point, self.rect)

    def getPos(self) -> QPoint:
        return self.rect.topLeft()

    def moveTo(self, pos: QPoint):
        self.rect.moveTo(pos)

    def moveBy(self, dx: int, dy: int):
        topLeft = self.rect.topLeft()
        newPoint = QPoint(topLeft.x() + dx, topLeft.y() + dy)

        self.rect.moveTopLeft(newPoint)

    def getEditMode(self, app) -> IEditState:
        return EditImageState(app, self)

    def getMemento(self):
        return ImageMemento(self, self.getRect(), self.getDrawContext())

    def getRect(self):
        return copy(self.rect)

    def setRect(self, rect: QRect):
        self.rect = rect
