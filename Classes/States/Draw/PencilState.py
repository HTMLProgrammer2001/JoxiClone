from typing import List
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QMouseEvent

from Classes.Commands.Create.CreatePencil import CreatePencil
from Classes.ObjectData.Pencil.Pencil import Pencil
from Classes.ObjectData.Pencil.PencilDrawContext import PencilDrawContext
from Classes.Toolbars.ObjectToolbars.PencilToolbar import PencilToolbar
from Intefaces.IState import IState


class PencilState(IState):
    points: List[QPoint] = []
    curPos: QPoint = None
    isDrawing = False

    def __init__(self, app):
        self.app = app
        self.points = []

        self.app.setToolbar(PencilToolbar())

    def mouseDown(self, event):
        self.isDrawing = True

    def mouseUp(self, event: QMouseEvent):
        self.points.append(event.pos())

        command = CreatePencil(self.app, self.points, self.createContext())
        command.execute()

        self.isDrawing = False
        self.points = []

        self.app.history.addCommand(command)

        self.app.repaint()

    def mouseMove(self, event: QMouseEvent):
        if self.isDrawing:
            self.curPos = event.pos()
            self.points.append(self.curPos)
            self.app.repaint()

    def paint(self, image):
        pencil = Pencil(self.points, self.createContext())
        pencil.draw(image)

    def createContext(self) -> PencilDrawContext:
        return self.app.contextToolbar.getContext()
