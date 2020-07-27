from Classes.ObjectData.Arrow.Arrow import Arrow
from Classes.States.Draw.LineState import LineState
from Classes.Commands.Create.CreateArrow import CreateArrow


class ArrowState(LineState):
    def paint(self, image):
        if not self.begin:
            return

        arrow = Arrow(self.begin, self.end, self.createContext())
        arrow.draw(image)

    def mouseUp(self, event):
        if self.isDrawing and self.end:
            context = self.createContext()

            command = CreateArrow(self.app, self.begin, self.end, context)
            command.execute()

            self.app.history.addCommand(command)

            self.isDrawing = False

            self.begin = None
            self.end = None
