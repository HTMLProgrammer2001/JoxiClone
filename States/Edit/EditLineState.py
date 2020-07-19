from PyQt5.QtGui import QPainter, QPen, QColor
from math import sqrt
import copy

from States.IState import IState
from Commands.Edit.EditLineCommand import EditLineCommand


class EditLineState(IState):
    editType = None

    def __init__(self, app):
        self.app = app
        self.curContext = copy.copy(app.selected.context)

    def mouseDown(self, event):
        pos = event.pos()
        begin = self.app.selected.context.begin
        end = self.app.selected.context.end

        if sqrt((pos.x() - begin.x())**2 + (pos.y() - begin.y())**2) <= 3:
            self.editType = 'BEGIN'
        elif sqrt((pos.x() - end.x())**2 + (pos.y() - end.y())**2) <= 3:
            self.editType = 'END'
        else:
            self.editType = 'NO'

    def mouseUp(self, event):
        command = EditLineCommand(self.app.selected, self.curContext, self.app.selected.context)
        command.execute()

        self.app.history.addCommand(command)

        if self.editType == 'NO':
            self.app.unSelect()

    def mouseMove(self, event):
        if not self.editType:
            return

        if self.editType == 'BEGIN':
            self.app.selected.context.setBegin(event.pos())
        elif self.editType == 'END':
            self.app.selected.context.setEnd(event.pos())

        self.app.repaint()

    def paint(self, image):
        qp = QPainter(image)

        qp.setPen(QPen(QColor('blue'), 1))

        qp.drawEllipse(self.app.selected.context.begin, 3, 3)
        qp.drawEllipse(self.app.selected.context.end, 3, 3)
