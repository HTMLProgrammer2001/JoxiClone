from PyQt5.QtCore import QRect

from Intefaces.IMemento import IMemento


class ImageMemento(IMemento):
    object = None

    def __init__(self, obj, rect: QRect, drawContext):
        self.object = obj
        self.rect = rect
        self.drawContext = drawContext

    def restore(self):
        self.object.setRect(self.rect)
        self.object.setDrawContext(self.drawContext)
