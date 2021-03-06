from PyQt5.QtCore import QRect, QPoint
from PyQt5.Qt import Qt
from PyQt5.Qt import QKeyEvent

from Classes.ObjectData.Rect.RectDrawContext import RectDrawContext
from Intefaces.IState import IState
from Classes.ObjectData.Rect.Rect import Rect
from Classes.Commands.Create.CreateRect import CreateRect
from Classes.Toolbars.ObjectToolbars.RectToolbar import RectToolbar
from Common.helpers import getBiggerDiff


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
            command = CreateRect(self.app, QRect(self.begin, self.end), self.createContext())
            command.execute()

            self.app.history.addCommand(command)

        self.isDrawing = False
        self.begin = None
        self.end = None

    def mouseMove(self, event: QKeyEvent):
        if not self.begin or not self.isDrawing:
            return

        end = event.pos()

        if event.modifiers() & Qt.ShiftModifier:
            # if shift then draw square with bigger size
            if getBiggerDiff(event.pos(), self.begin) == 'X':
                end = QPoint(end.x(), end.x() - self.begin.x() + self.begin.y())
            else:
                end = QPoint(end.y() - self.begin.y() + self.begin.x(), end.y())

        if event.modifiers() & Qt.AltModifier:
            # calculate new end point
            newEndX = end.x() + (end.x() - self.begin.x())
            newEndY = end.y() + (end.y() - self.begin.y())

            end = QPoint(newEndX, newEndY)

        self.end = end
        self.app.repaint()

    def paint(self, image):
        if not self.begin or not self.end:
            return

        rect = Rect(QRect(self.begin, self.end), self.createContext())
        rect.draw(image)

    def createContext(self) -> RectDrawContext:
        return self.app.contextToolbar.getContext()
