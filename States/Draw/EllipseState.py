from PyQt5.QtCore import Qt, QPoint

from States.IState import IState
from Objects.Ellipse import Ellipse
from Commands.Create.CreateEllipse import CreateEllipse
from Context.ObjectData.EllipseContext import EllipseContext
from Toolbars.ObjectToolbars.EllipseToolbar import EllipseToolbar


class EllipseState(IState):
    begin = None
    isDrawing = False
    end = None

    def __init__(self, app):
        self.app = app

        self.app.setToolbar(EllipseToolbar())

    def mouseDown(self, event):
        self.begin = event.pos()
        self.isDrawing = True

    def mouseUp(self, event):
        if self.isDrawing and self.end:
            context = self.createContext()

            command = CreateEllipse(self.app, context)
            command.execute()

            self.app.history.addCommand(command)

            self.isDrawing = False

            self.begin = None
            self.end = None

    def mouseMove(self, event):
        end = event.pos()

        if event.modifiers() & Qt.ShiftModifier:
            # if shift then draw circle with bigger side
            if abs(event.pos().x() - self.begin.x()) > abs(event.pos().y() - self.begin.y()):
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
        if not self.begin:
            return

        circle = Ellipse(self.createContext())
        circle.draw(image)

    def createContext(self) -> EllipseContext:
        context = EllipseContext(self.begin)

        context.setRadiusX(abs(self.end.x() - self.begin.x()))
        context.setRadiusY(abs(self.end.y() - self.begin.y()))
        context.setDraw(self.app.contextToolbar.getContext())

        return context
