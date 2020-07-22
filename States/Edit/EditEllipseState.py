from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import QPoint
from math import sqrt
from copy import copy

from States.IState import IState
from States.Edit.IEditState import IEditState
from Commands.EditCommand import EditCommand
from Toolbars.IToolbar import IToolbar
from Toolbars.EllipseToolbar import EllipseToolbar


class EditEllipseState(IEditState, IState):
    editType = None

    def mouseDown(self, event):
        context = self.selected.context
        point = self.selected.context.center - QPoint(0, context.radiusY)

        if sqrt((event.pos().x() - point.x())**2 + (event.pos().y() - point.y())**2) <= 3:
            self.editType = 'TOP'
        else:
            self.editType = 'NO'

    def mouseUp(self, event):
        command = EditCommand(self.selected, self.curContext, self.selected.context)
        command.execute()

        self.app.history.addCommand(command)

        if self.editType == 'NO':
            self.app.unSelect()

    def mouseMove(self, event):
        if not self.editType:
            return

        if self.editType == 'TOP':
            radPoint = event.pos() - self.curContext.center
            self.selected.context.setRadiusX(radPoint.x())
            self.selected.context.setRadiusY(radPoint.y())

        self.app.repaint()

    def paint(self, image):
        center = self.selected.context.center
        radiusY = self.selected.context.radiusY

        qp = QPainter(image)
        qp.setPen(QPen(QColor('blue'), 1))
        qp.drawEllipse(center - QPoint(0, radiusY), 3, 3)

    def changeDraw(self, newDraw):
        self.selected.context.setDraw(newDraw)

        self.execChange()
        self.app.repaint()

    def execChange(self):
        command = EditCommand(self.selected, self.curContext, self.selected.context)
        command.execute()

        self.app.history.addCommand(command)
        self.curContext = copy(self.selected.context)

    def getToolbar(self) -> IToolbar:
        return EllipseToolbar()
