from typing import List, Union
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QPainter, QPen, QColor, QMouseEvent

from Classes.ObjectData.Pen.PenMemento import PenMemento
from Classes.Toolbars.ObjectToolbars.PenToolbar import PenToolbar
from Intefaces.IEditState import IEditState
from Intefaces.IToolbar import IToolbar
from Common.helpers import getDistance


class EditPenState(IEditState):
    selected = None
    curMemento: PenMemento = None
    editType: Union[str, QPoint] = None

    def mouseDown(self, event: QMouseEvent):
        pos = event.pos()
        points: List[QPoint] = self.selected.points

        for point in points:
            if getDistance(pos, point) <= 3:
                if event.button() == Qt.RightButton:
                    self.selected.points.remove(point)
                else:
                    self.editType = point
                break
        else:
            self.editType = 'NO'

    def mouseMove(self, event):
        if not self.editType:
            return

        self.editType.setX(event.pos().x())
        self.editType.setY(event.pos().y())

        self.app.repaint()

    def getToolbar(self) -> IToolbar:
        return PenToolbar()

    def paint(self, image):
        qp = QPainter(image)

        qp.setPen(QPen(QColor('blue'), 1))

        for point in self.selected.points:
            qp.drawEllipse(point, 3, 3)
