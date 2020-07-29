from typing import List
from PyQt5.QtCore import QPoint

from Intefaces.IMemento import IMemento


class PenMemento(IMemento):
    object = None

    def __init__(self, object, polygon: List[QPoint], drawContext):
        super().__init__(object)

        self.polygon = polygon
        self.drawContext = drawContext

    def restore(self):
        self.object.setPoints(self.polygon)
        self.object.setDrawContext(self.drawContext)
