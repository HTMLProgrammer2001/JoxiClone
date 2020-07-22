from PyQt5.QtCore import QRect, QPoint
from PyQt5.Qt import Qt
from PyQt5.Qt import QKeyEvent

from States.IState import IState
from Objects.Rect import Rect
from Commands.Create.CreateRect import CreateRect
from Context.ObjectData.RectContext import RectContext
from Toolbars.RectToolbar import RectToolbar


class RectState(IState):
    begin = None
    end = None
    isDrawing = False

    def __init__(self, app):
        self.app = app

        self.app.setToolbar(RectToolbar())

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

    def mouseMove(self, event: QKeyEvent):
        if event.modifiers() & Qt.ShiftModifier:
            # if shift then draw square with bigger size
            if abs(event.pos().x() - self.begin.x()) > abs(event.pos().y() - self.begin.y()):
                self.end = QPoint(event.pos().x(), event.pos().x() - self.begin.x() + self.begin.x())
            else:
                self.end = QPoint(event.pos().y() - self.begin.y() + self.begin.y(), event.pos().y())

            self.app.repaint()

        elif event.modifiers() & Qt.AltModifier:
            # calculate new end point
            newEndX = event.pos().x() + (event.pos().x() - self.begin.x())
            newEndY = event.pos().y() + (event.pos().y() - self.begin.y())

            self.end = QPoint(newEndX, newEndY)

            # repaint
            self.app.repaint()
        else:
            # simple rectangle
            self.end = event.pos()
            self.app.repaint()

    def paint(self, image):
        if not self.begin:
            return

        rect = Rect(self.createContext())
        rect.draw(image)

    def createContext(self) -> RectContext:
        drawContext = self.app.contextToolbar.getContext()
        context = RectContext(QRect(self.begin, self.end), drawContext)

        return context
