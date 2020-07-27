from PyQt5.QtCore import QRect

from Intefaces.IMemento import IMemento


class RectMemento(IMemento):
    object = None

    def __init__(self, object, rect: QRect, drawContext):
        super().__init__(object)

        self.rect = rect
        self.drawContext = drawContext

    def restore(self):
        self.object.setRect(self.rect)
        self.object.setDrawContext(self.drawContext)
