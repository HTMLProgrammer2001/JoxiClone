from PyQt5.QtGui import QPainter, QPen, QColor
from math import sqrt
from copy import copy

from States.IState import IState
from States.Edit.IEditState import IEditState
from Commands.EditCommand import EditCommand
from Context.DrawData.LineDrawContext import LineDrawContext
from Toolbars.LineToolbar import LineToolbar
from Toolbars.IToolbar import IToolbar


class EditLineState(IEditState, IState):
    def mouseDown(self, event):
        pos = event.pos()
        begin = self.selected.context.begin
        end = self.selected.context.end

        if sqrt((pos.x() - begin.x())**2 + (pos.y() - begin.y())**2) <= 3:
            self.editType = 'BEGIN'
        elif sqrt((pos.x() - end.x())**2 + (pos.y() - end.y())**2) <= 3:
            self.editType = 'END'
        else:
            self.editType = 'NO'

    def mouseMove(self, event):
        if not self.editType:
            return

        if self.editType == 'BEGIN':
            self.selected.context.setBegin(event.pos())
        elif self.editType == 'END':
            self.selected.context.setEnd(event.pos())

        self.app.repaint()

    def paint(self, image):
        qp = QPainter(image)

        qp.setPen(QPen(QColor('blue'), 1))

        qp.drawEllipse(self.selected.context.begin, 3, 3)
        qp.drawEllipse(self.selected.context.end, 3, 3)

    def execChange(self):
        command = EditCommand(self.selected, self.curContext, self.selected.context)
        command.execute()

        self.app.history.addCommand(command)
        self.curContext = copy(self.selected.context)

    def changeDraw(self, newDraw: LineDrawContext):
        print(newDraw)

        self.selected.context.setDraw(newDraw)

        self.execChange()
        self.app.repaint()

    def getToolbar(self) -> IToolbar:
        return LineToolbar()
