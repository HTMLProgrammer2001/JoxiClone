from PyQt5.QtGui import QPainter, QPen, QColor
from math import sqrt
import copy

from States.IState import IState
from Commands.EditCommand import EditCommand


class EditRectState(IState):
    editType = None

    def __init__(self, app):
        self.app = app
        self.curContext = copy.copy(app.selected.context)

    def mouseDown(self, event):
        botRight = self.app.selected.context.rect.bottomRight()
        topLeft = self.app.selected.context.rect.topLeft()

        if sqrt((event.pos().x() - botRight.x())**2 + (event.pos().y() - botRight.y())**2) <= 3:
            self.editType = 'BOTTOMRIGHT'
        elif sqrt((event.pos().x() - topLeft.x())**2 + (event.pos().y() - topLeft.y())**2) <= 3:
            self.editType = 'TOPLEFT'
        else:
            self.editType = 'NO'

    def mouseUp(self, event):
        command = EditCommand(self.app.selected, self.curContext, self.app.selected.context)
        command.execute()

        self.app.history.addCommand(command)

        if self.editType == 'NO':
            self.app.unSelect()

    def mouseMove(self, event):
        if not self.editType:
            return

        print('Edit type: ', self.editType)

        rect = copy.copy(self.app.selected.context.rect)

        if self.editType == 'BOTTOMRIGHT':
            rect.setBottomRight(event.pos())
        elif self.editType == 'TOPLEFT':
            rect.setTopLeft(event.pos())

        self.app.selected.context.setRect(rect)
        self.app.repaint()

    def paint(self, image):
        context = self.app.selected.context

        qp = QPainter(image)
        qp.setPen(QPen(QColor('blue'), 1))

        qp.drawEllipse(context.rect.bottomRight(), 3, 3)
        qp.drawEllipse(context.rect.topLeft(), 3, 3)
