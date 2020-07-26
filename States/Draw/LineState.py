from PyQt5.Qt import QKeyEvent
from PyQt5.Qt import Qt
from PyQt5.QtCore import QPoint

from Context.LineDrawContext import LineDrawContext
from States.IState import IState
from Objects.Line import Line
from Commands.Create.CreateLine import CreateLine
from Toolbars.ObjectToolbars.LineToolbar import LineToolbar
from helpers import getBiggerDiff


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

            command = CreateLine(self.app, self.begin, self.end, context)
            command.execute()

            self.app.history.addCommand(command)

            self.isDrawing = False

            self.begin = None
            self.end = None

    def mouseMove(self, event: QKeyEvent):
        if event.modifiers() == Qt.ShiftModifier:

            if getBiggerDiff(event.pos(), self.begin) == 'X':
                self.end = QPoint(event.pos().x(), self.begin.y())
            else:
                self.end = QPoint(self.begin.x(), event.pos().y())

        else:
            self.end = event.pos()

        self.app.repaint()

    def paint(self, image):
        if not self.begin:
            return

        line = Line(self.begin, self.end, self.createContext())
        line.draw(image)

    def createContext(self) -> LineDrawContext:
        return self.app.contextToolbar.getContext()
