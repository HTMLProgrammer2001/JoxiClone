from States.IState import IState
from Objects.Ellipse import Ellipse
from Commands.Create.CreateEllipse import CreateEllipse
from Context.ObjectData.EllipseContext import EllipseContext
from Toolbars.EllipseToolbar import EllipseToolbar


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
        self.end = event.pos()
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
