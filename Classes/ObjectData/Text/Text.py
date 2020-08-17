from copy import copy

from PyQt5.QtCore import QPoint, QRect
from PyQt5.QtGui import QPainter, QFontMetrics, QPen

from Classes.ObjectData.Text.TextDrawContext import TextDrawContext
from Classes.ObjectData.Text.TextMemento import TextMemento
from Classes.States.Edit.EditTextState import EditTextState
from Intefaces.IEditState import IEditState
from Intefaces.IObject import IObject
from Common.helpers import rectContain


class Text(IObject):
    def __init__(self, pos: QPoint, text: str, drawContext: TextDrawContext):
        self.text = text
        self.pos = pos
        self.drawContext = drawContext

    def draw(self, image):
        qp = QPainter(image)

        qp.setPen(QPen(self.drawContext.stroke, 1))
        qp.setFont(self.drawContext.font)

        qp.drawText(self.pos.x(), self.pos.y(), self.text)

    def contain(self, point: QPoint) -> bool:
        return rectContain(point, self.getRect())

    def getRect(self) -> QRect:
        fm = QFontMetrics(self.drawContext.font)
        rect: QRect = fm.boundingRect(self.text)
        rect.moveTopLeft(self.getPos() - QPoint(0, fm.height()))

        return rect

    def getPos(self):
        return copy(self.pos)

    def getText(self):
        return self.text

    def setText(self, text: str):
        self.text = text

    def moveTo(self, pos: QPoint):
        self.pos = pos

    def moveBy(self, dx: int, dy: int):
        self.pos = self.pos + QPoint(dx, dy)

    def getEditMode(self, app) -> IEditState:
        return EditTextState(app, self)

    def setPos(self, pos: QPoint):
        self.pos = pos

    def getMemento(self):
        return TextMemento(self, self.getPos(), self.getText(), self.getDrawContext())
