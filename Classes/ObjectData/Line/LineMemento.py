from PyQt5.QtCore import QPoint

from Intefaces.IMemento import IMemento


class LineMemento(IMemento):
    object = None

    def __init__(self, object, begin: QPoint, end: QPoint, drawContext):
        super().__init__(object)

        self.begin = begin
        self.end = end
        self.drawContext = drawContext

    def restore(self):
        self.object.setBegin(self.begin)
        self.object.setEnd(self.end)
        self.object.setDrawContext(self.drawContext)
