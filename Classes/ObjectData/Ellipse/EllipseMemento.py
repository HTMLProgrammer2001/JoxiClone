from PyQt5.QtCore import QPoint

from Intefaces.IMemento import IMemento


class EllipseMemento(IMemento):
    object = None

    def __init__(self, object, center: QPoint, radX: int, radY: int, drawContext):
        super().__init__(object)

        self.center = center
        self.radiusX = radX
        self.radiusY = radY
        self.drawContext = drawContext

    def restore(self):
        self.object.setCenter(self.center)
        self.object.setRadiusX(self.radiusX)
        self.object.setRadiusY(self.radiusY)
        self.object.setDrawContext(self.drawContext)
