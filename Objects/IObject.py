from abc import abstractmethod
from PyQt5.QtCore import QPoint


class IObject:
    context = None

    @abstractmethod
    def draw(self, image):
        pass

    def setContext(self, context):
        self.context = context

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
