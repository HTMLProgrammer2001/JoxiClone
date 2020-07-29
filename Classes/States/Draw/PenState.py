from typing import List

from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QPolygon, QMouseEvent

from Classes.Commands.Create.CreatePen import CreatePen
from Classes.ObjectData.Pen.Pen import Pen
from Classes.ObjectData.Pen.PenDrawContext import PenDrawContext
from Classes.Toolbars.ObjectToolbars.PenToolbar import PenToolbar
from Intefaces.IState import IState


class PenState(IState):
    points: List[QPoint] = []
    curPos: QPoint = None
    isDrawing = False

    def __init__(self, app):
        self.app = app

        self.app.setToolbar(PenToolbar())

    def mouseDown(self, event):
        self.isDrawing = True

    def mouseUp(self, event: QMouseEvent):
        self.points.append(event.pos())

        if event.button() == Qt.RightButton:
            event.ignore()

            command = CreatePen(self.app, self.points, self.createContext())
            command.execute()

            self.isDrawing = False
            self.points = []

            self.app.history.addCommand(command)

        self.app.repaint()

    def mouseMove(self, event: QMouseEvent):
        self.curPos = event.pos()
        self.app.repaint()

    def paint(self, image):
        if len(self.points) <= 1:
            return

        pen = Pen([*self.points, self.curPos], self.createContext())
        pen.draw(image)

    def createContext(self) -> PenDrawContext:
        return self.app.contextToolbar.getContext()
