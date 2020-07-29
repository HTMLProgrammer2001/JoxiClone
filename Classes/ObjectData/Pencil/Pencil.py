from PyQt5.QtGui import QPainter, QPen, QPolygon

from Classes.ObjectData.Pen.Pen import Pen
from Classes.ObjectData.Pencil.PencilMemento import PencilMemento
from Classes.States.Edit.EditPencilState import EditPencilState
from Intefaces.IEditState import IEditState


class Pencil(Pen):
    def getMemento(self) -> PencilMemento:
        return PencilMemento(self, self.getPoints(), self.getDrawContext())

    def getEditMode(self, app) -> IEditState:
        return EditPencilState(app, self)

    def draw(self, image):
        qp = QPainter(image)

        qp.setPen(QPen(self.drawContext.stroke, self.drawContext.width))
        qp.drawPolyline(QPolygon(self.points))
