from Commands.ICommand import ICommand
from Context.LineContext import LineContext
from Objects.Line import Line
from history import History


class CreateLine(ICommand):
    def __init__(self, app, context: LineContext):
        self.app = app
        self.context = context
        self.line = None

    def execute(self):
        self.line = Line(self.context)
        self.app.objects.append(self.line)
        self.app.repaint()

    def unexecute(self):
        self.app.objects.remove(self.line)
        self.app.repaint()
