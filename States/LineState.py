from PyQt5.QtGui import QPen

from States.IState import IState
from Objects.Line import Line
from Commands.Create.CreateLine import CreateLine
from Context.LineContext import LineContext


class LineState(IState):
    begin = None
    end = None
    isDrawing = False

    def mouseDown(self, event):
        self.begin = event.pos()
        self.isDrawing = True

    def mouseUp(self, event):
        if self.isDrawing and self.end:
            context = self.createContext()

            command = CreateLine(self.app, context)
            command.execute()

            self.app.history.addCommand(command)

            self.isDrawing = False

            self.begin = None
            self.end = None

    def mouseMove(self, event):
        self.end = event.pos()
        self.app.repaint()

    def paint(self, image):
        if not self.begin:
            return

        line = Line(self.createContext())
        line.draw(image)

    def createContext(self) -> LineContext:
        context = LineContext(self.begin, self.end)
        context.setPen(QPen(self.app.brushColor, self.app.brushSize))

        return context
