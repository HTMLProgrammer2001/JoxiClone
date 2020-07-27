from abc import abstractmethod
from copy import copy
from PyQt5.QtCore import QPoint

from Intefaces.IEditState import IEditState


class IObject:
    drawContext = None

    @abstractmethod
    def draw(self, image):
        pass

    @abstractmethod
    def getMemento(self):
        pass

    def setDrawContext(self, context):
        self.drawContext = context

    def getDrawContext(self):
        return copy(self.drawContext)

    @abstractmethod
    def contain(self, point: QPoint) -> bool:
        pass

    @abstractmethod
    def getPos(self) -> QPoint:
        pass

    @abstractmethod
    def moveTo(self, pos: QPoint):
        pass

    @abstractmethod
    def moveBy(self, dx: int, dy: int):
        pass

    @abstractmethod
    def getEditMode(self, app) -> IEditState:
        pass
