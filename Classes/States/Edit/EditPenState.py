from PyQt5.QtGui import QPainter, QPen, QColor

from Classes.ObjectData.Pen.PenMemento import PenMemento
from Intefaces.IEditState import IEditState
from helpers import getDistance


class EditPenState(IEditState):
    selected = None
    curMemento: PenMemento = None

    def mouseDown(self, event):
        pos = event.pos()
        polygon = self.selected.polygon

        for i in range(0, len(polygon)):
            if getDistance(pos, polygon.point(i)) <= 3:
                self.editType = i
                break
        else:
            self.editType = 'NO'

    def paint(self, image):
        qp = QPainter(image)

        qp.setPen(QPen(QColor('blue'), 1))

        for index in range(0, len(self.selected.polygon)):
            qp.drawEllipse(self.selected.polygon.point(index), 3, 3)
