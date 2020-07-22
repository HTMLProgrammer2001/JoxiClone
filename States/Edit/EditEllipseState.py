from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import QPoint
from math import sqrt

from States.IState import IState
from States.Edit.IEditState import IEditState
from Commands.EditCommand import EditCommand


class EditCircleState(IEditState, IState):
    editType = None

    def mouseDown(self, event):
        context = self.selected.context
        point = self.selected.context.center - QPoint(0, context.radius)

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
            self.selected.context.setRadius(radPoint.y())

        self.app.repaint()

    def paint(self, image):
        center = self.selected.context.center
        radius = self.selected.context.radius

        qp = QPainter(image)
        qp.setPen(QPen(QColor('blue'), 1))
        qp.drawEllipse(center - QPoint(0, radius), 3, 3)
