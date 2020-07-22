from PyQt5.Qt import QKeyEvent
from PyQt5.Qt import Qt
from PyQt5.QtCore import QPoint

from States.IState import IState
from Objects.Line import Line
from Commands.Create.CreateLine import CreateLine
from Context.ObjectData.LineContext import LineContext
from Toolbars.LineToolbar import LineToolbar


class LineState(IState):
    begin = None
    end = None
    isDrawing = False

    def __init__(self, app):
        self.app = app

        self.app.setToolbar(LineToolbar())

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

    def mouseMove(self, event: QKeyEvent):
        if event.modifiers() == Qt.ShiftModifier:

            if abs(event.pos().x() - self.begin.x()) > abs(event.pos().y() - self.begin.y()):
                self.end = QPoint(event.pos().x(), self.begin.y())
            else:
                self.end = QPoint(self.begin.x(), event.pos().y())

        else:
            self.end = event.pos()

        self.app.repaint()

    def paint(self, image):
        if not self.begin:
            return

        line = Line(self.createContext())
        line.draw(image)

    def createContext(self) -> LineContext:
        context = LineContext(self.begin, self.end, self.app.contextToolbar.getContext())

        return context
