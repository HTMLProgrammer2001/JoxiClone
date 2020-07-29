from PyQt5.QtGui import QPainter, QPen, QColor, QPolygon

from Classes.Toolbars.ObjectToolbars.PencilToolbar import PencilToolbar
from Intefaces.IEditState import IEditState
from Intefaces.IToolbar import IToolbar


class EditPencilState(IEditState):
    def getToolbar(self) -> IToolbar:
        return PencilToolbar()

    def paint(self, image):
        qp = QPainter(image)

        qp.setPen(QPen(QColor('blue'), 1))
        qp.drawRect(QPolygon(self.selected.getPoints()).boundingRect())
