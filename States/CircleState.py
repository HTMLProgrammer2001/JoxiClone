from PyQt5.QtGui import QPen

from States.IState import IState
from Commands.Create.CreateCircle import CreateCircle
from Context.CircleContext import CircleContext


class CircleState(IState):
    begin = None
    isDrawing = False

    def mouseDown(self, event):
        self.begin = event.pos()
        self.isDrawing = True

    def mouseUp(self, event):
        if self.isDrawing:
            context = CircleContext(self.begin)
            context.setRadius(max(abs(event.pos().x() - self.begin.x()), abs(event.pos().y() - self.begin.y())))
            context.setPen(QPen(self.app.brushColor, self.app.brushSize))

            command = CreateCircle(self.app, context)
            command.execute()

            self.app.history.addCommand(command)

            self.isDrawing = False

    def mouseMove(self, event):
        pass
