from PyQt5.QtGui import QPen

from States.IState import IState
from Objects.Circle import Circle
from Commands.Create.CreateCircle import CreateCircle
from Context.ObjectData.CircleContext import CircleContext


class CircleState(IState):
    begin = None
    isDrawing = False
    end = None

    def mouseDown(self, event):
        self.begin = event.pos()
        self.isDrawing = True

    def mouseUp(self, event):
        if self.isDrawing and self.end:
            context = self.createContext()

            command = CreateCircle(self.app, context)
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

        circle = Circle(self.createContext())
        circle.draw(image)

    def createContext(self) -> CircleContext:
        context = CircleContext(self.begin)
        context.setRadius(max(abs(self.end.x() - self.begin.x()), abs(self.end.y() - self.begin.y())))
        context.setPen(QPen(self.app.brushColor, self.app.brushSize))

        return context
