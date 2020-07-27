from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import QPoint, Qt

from Classes.ObjectData.Ellipse.EllipseMemento import EllipseMemento
from Intefaces.IState import IState
from Intefaces.IEditState import IEditState
from Classes.Commands.EditCommand import EditCommand
from Intefaces.IToolbar import IToolbar
from Classes.Toolbars.ObjectToolbars.EllipseToolbar import EllipseToolbar
from helpers import getDistance


class EditEllipseState(IEditState, IState):
    editType = None
    selected = None
    curMemento: EllipseMemento = None

    def mouseDown(self, event):
        point = self.selected.getCenter() - QPoint(0, self.selected.getRadiusY())

        if getDistance(point, event.pos()) <= 3:
            self.editType = 'TOP'
        else:
            self.editType = 'NO'

    def mouseUp(self, event):
        command = EditCommand(self.curMemento, self.selected.getMemento())
        command.execute()

        self.app.history.addCommand(command)

        if self.editType == 'NO':
            self.app.unSelect()

    def mouseMove(self, event):
        if not self.editType:
            return

        if self.editType == 'TOP':
            radPoint = event.pos() - self.curMemento.center

            if event.modifiers() & Qt.ShiftModifier:
                self.selected.setRadiusX(max(radPoint.x(), radPoint.y()))
                self.selected.setRadiusY(max(radPoint.y(), radPoint.x()))
            else:
                self.selected.setRadiusX(radPoint.x())
                self.selected.setRadiusY(radPoint.y())

        self.app.repaint()

    def paint(self, image):
        center = self.selected.getCenter()
        radiusY = self.selected.getRadiusY()

        qp = QPainter(image)
        qp.setPen(QPen(QColor('blue'), 1))
        qp.drawEllipse(center - QPoint(0, radiusY), 3, 3)

    def changeDraw(self, newDraw):
        self.selected.setDrawContext(newDraw)

        self.execChange()
        self.app.repaint()

    def getToolbar(self) -> IToolbar:
        return EllipseToolbar()
