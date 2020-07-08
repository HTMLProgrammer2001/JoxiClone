from PyQt5.QtGui import QPen

from States.IState import IState
from Commands.Create.CreateLine import CreateLine
from Context.LineContext import LineContext


class LineState(IState):
    begin = None
    isDrawing = False

    def mouseDown(self, event):
        self.begin = event.pos()
        self.isDrawing = True

    def mouseUp(self, event):
        if self.isDrawing:
            context = LineContext(self.begin, event.pos())
            context.setPen(QPen(self.app.brushColor, self.app.brushSize))

            command = CreateLine(self.app, context)
            command.execute()

            self.app.history.addCommand(command)

            self.isDrawing = False

    def mouseMove(self, event):
        pass
