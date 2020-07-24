from PyQt5.QtCore import QPoint, QRect, Qt
from PyQt5.QtGui import QPainter, QPen, QColor
from math import sqrt
import copy

from States.IState import IState
from States.Edit.IEditState import IEditState
from Commands.EditCommand import EditCommand
from Toolbars.ObjectToolbars.RectToolbar import RectToolbar
from Toolbars.IToolbar import IToolbar


class EditRectState(IEditState, IState):
    editType = None

    def mouseDown(self, event):
        botRight = self.selected.context.rect.bottomRight()
        topLeft = self.selected.context.rect.topLeft()

        if sqrt((event.pos().x() - botRight.x())**2 + (event.pos().y() - botRight.y())**2) <= 3:
            self.editType = 'BOTTOMRIGHT'
        elif sqrt((event.pos().x() - topLeft.x())**2 + (event.pos().y() - topLeft.y())**2) <= 3:
            self.editType = 'TOPLEFT'
        else:
            self.editType = 'NO'

    def mouseMove(self, event):
        if not self.editType:
            return

        rect: QRect = copy.copy(self.selected.context.rect)
        endPoint = event.pos()

        if self.editType == 'BOTTOMRIGHT':
            if event.modifiers() & Qt.ShiftModifier:
                diff = rect.bottomRight() - event.pos()
                maxVal = min(diff.x(), diff.y())
                endPoint = QPoint(maxVal, maxVal)

            rect.setBottomRight(endPoint)

        elif self.editType == 'TOPLEFT':
            if event.modifiers() & Qt.ShiftModifier:
                diff = event.pos() - rect.bottomRight()
                minVal = min(diff.x(), diff.y())
                endPoint = QPoint(minVal, minVal)

            rect.setTopLeft(endPoint)

        self.selected.context.setRect(rect)
        self.app.repaint()

    def paint(self, image):
        context = self.selected.context

        qp = QPainter(image)
        qp.setPen(QPen(QColor('blue'), 1))

        qp.drawEllipse(context.rect.bottomRight(), 3, 3)
        qp.drawEllipse(context.rect.topLeft(), 3, 3)

    def execChange(self):
        command = EditCommand(self.selected, self.curContext, self.selected.context)
        command.execute()

        self.app.history.addCommand(command)
        self.curContext = copy.copy(self.selected.context)

    def changeDraw(self, newDraw):
        self.selected.context.setDraw(newDraw)

        self.execChange()
        self.app.repaint()

    def getToolbar(self) -> IToolbar:
        return RectToolbar()
