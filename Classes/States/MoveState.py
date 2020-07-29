from PyQt5.QtCore import QPoint
from typing import Optional

from Classes.Toolbars.NoneToolbar import NoneToolbar
from Intefaces.IState import IState
from Intefaces.IObject import IObject
from Classes.Commands.MoveCommand import MoveCommand


class MoveState(IState):
    selected: Optional[IObject] = None
    lastPosition: Optional[QPoint] = None
    startPosition: Optional[QPoint] = None

    isMoved: bool = False

    def __init__(self, app):
        super().__init__(app)

        self.app.setToolbar(NoneToolbar())

    def paint(self, image):
        pass

    def mouseDown(self, event):
        self.isMoved = False

        for obj in reversed(self.app.objects):
            if obj.contain(event.pos()):
                self.selected = obj
                self.lastPosition = event.pos()
                self.startPosition = obj.getPos()
                break
        else:
            self.selected = None
            self.lastPosition = None
            self.startPosition = None

    def mouseUp(self, event):
        if not self.startPosition:
            return

        if not self.isMoved:
            self.app.select(self.selected)
            self.app.repaint()
            return

        command = MoveCommand(self.selected, self.startPosition, self.selected.getPos())
        self.app.history.addCommand(command)

        self.selected = None

    def mouseMove(self, event):
        if self.selected:
            pos = event.pos()

            self.selected.moveBy(pos.x() - self.lastPosition.x(), pos.y() - self.lastPosition.y())

            self.lastPosition = pos
            self.app.repaint()

            self.isMoved = True
