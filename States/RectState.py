from PyQt5.QtCore import QRect
from PyQt5.QtGui import QPen

from States.IState import IState
from Commands.Create.CreateRect import CreateRect
from Context.RectContext import RectContext


class RectState(IState):
    begin = None
    isDrawing = False

    def mouseDown(self, event):
        self.begin = event.pos()
        self.isDrawing = True

    def mouseUp(self, event):
        if self.isDrawing:
            context = RectContext(QRect(self.begin, event.pos()))
            context.setFill(True)
            context.setPen(QPen(self.app.brushColor, self.app.brushSize))

            command = CreateRect(self.app, context)
            command.execute()

            self.app.history.addCommand(command)

            self.isDrawing = False

    def mouseMove(self, event):
        pass
