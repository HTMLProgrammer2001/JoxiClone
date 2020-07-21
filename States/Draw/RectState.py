from PyQt5.QtCore import QRect
from PyQt5.QtGui import QPen

from States.IState import IState
from Objects.Rect import Rect
from Commands.Create.CreateRect import CreateRect
from Context.ObjectData.RectContext import RectContext


class RectState(IState):
    begin = None
    end = None
    isDrawing = False

    def mouseDown(self, event):
        self.begin = event.pos()
        self.isDrawing = True

    def mouseUp(self, event):
        if self.isDrawing and self.end:
            context = self.createContext()

            command = CreateRect(self.app, context)
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

        rect = Rect(self.createContext())
        rect.draw(image)

    def createContext(self) -> RectContext:
        context = RectContext(QRect(self.begin, self.end))
        context.setFill(True)
        context.setPen(QPen(self.app.brushColor, self.app.brushSize))

        return context
