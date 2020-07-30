from PyQt5.QtCore import QPoint

from Intefaces.IMemento import IMemento


class TextMemento(IMemento):
    object = None

    def __init__(self, object, pos: QPoint, text: str, drawContext):
        super().__init__(object)

        self.pos = pos
        self.text = text
        self.drawContext = drawContext

    def restore(self):
        self.object.setPos(self.pos)
        self.object.setText(self.text)
        self.object.setDrawContext(self.drawContext)
