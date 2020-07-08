from abc import abstractmethod
from PyQt5.QtCore import QPoint


class IObject:
    @abstractmethod
    def draw(self, image):
        pass

    @abstractmethod
    def contain(self, point: QPoint) -> bool:
        pass
