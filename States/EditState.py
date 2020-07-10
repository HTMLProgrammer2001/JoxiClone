from PyQt5.QtCore import QPoint
from typing import List, Optional

from States.IState import IState
from Objects.IObject import IObject
from Commands.MoveCommand import MoveCommand


class EditState(IState):
    selected: Optional[IObject] = None
    lastPosition: Optional[QPoint] = None
    startPosition: Optional[QPoint] = None

    def mouseDown(self, event):
        for obj in reversed(self.app.objects):
            if obj.contain(event.pos()):
                self.selected = obj
                self.lastPosition = event.pos()
                self.startPosition = event.pos()
                break
        else:
            self.selected = None
            self.lastPosition = None
            self.startPosition = None

    def mouseUp(self, event):
        if not self.startPosition:
            return

        print(self.startPosition, self.lastPosition)

        command = MoveCommand(self.selected, self.startPosition, self.lastPosition)
        self.app.history.addCommand(command)

    def mouseMove(self, event):
        if self.selected:
            pos = event.pos()

            self.selected.moveBy(pos.x() - self.lastPosition.x(), pos.y() - self.lastPosition.y())

            self.lastPosition = pos
            self.app.repaint()
