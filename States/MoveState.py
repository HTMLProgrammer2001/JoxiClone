from PyQt5.QtCore import QPoint
from typing import Optional

from States.IState import IState
from Objects.IObject import IObject
from Commands.MoveCommand import MoveCommand


class MoveState(IState):
    selected: Optional[IObject] = None
    lastPosition: Optional[QPoint] = None
    startPosition: Optional[QPoint] = None

    isMoved: bool = False

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

    def mouseMove(self, event):
        if self.selected:
            pos = event.pos()

            self.selected.moveBy(pos.x() - self.lastPosition.x(), pos.y() - self.lastPosition.y())

            self.lastPosition = pos
            self.app.repaint()

            self.isMoved = True
