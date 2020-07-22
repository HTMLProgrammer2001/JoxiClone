from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.Qt import QKeyEvent
from PyQt5.QtCore import QPoint
from PyQt5.Qt import Qt
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

    def mouseMove(self, event: QKeyEvent):
        if not self.editType:
            return

        begin = self.selected.context.begin
        end = self.selected.context.end

        newPoint: QPoint = event.pos()

        if self.editType == 'BEGIN':
            # Shift pressed
            if event.modifiers() == Qt.ShiftModifier:
                # Parallel to x axis
                if abs(begin.x() - event.pos().x()) > abs(begin.y() - event.pos().y()):
                    newPoint = QPoint(event.pos().x(), end.y())
                else:
                    # Parallel to Y axis
                    newPoint = QPoint(end.x(), event.pos().y())

            self.selected.context.setBegin(newPoint)

        elif self.editType == 'END':
            # Shift pressed
            if event.modifiers() == Qt.ShiftModifier:
                # Parallel to x axis
                if abs(end.x() - event.pos().x()) > abs(end.y() - event.pos().y()):
                    newPoint = QPoint(event.pos().x(), begin.y())
                else:
                    # Parallel to y axis
                    newPoint = QPoint(begin.x(), event.pos().y())

            self.selected.context.setEnd(newPoint)

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
        self.selected.context.setDraw(newDraw)

        self.execChange()
        self.app.repaint()

    def getToolbar(self) -> IToolbar:
        return LineToolbar()
