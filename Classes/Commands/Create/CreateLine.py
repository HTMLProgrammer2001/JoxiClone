from Intefaces.ICommand import ICommand
from Classes.ObjectData.Line.LineDrawContext import LineDrawContext
from Classes.ObjectData.Line.Line import Line


class CreateLine(ICommand):
    line = None

    def __init__(self, app, begin, end, context: LineDrawContext):
        self.app = app
        self.begin = begin
        self.end = end
        self.drawContext = context

    def execute(self):
        self.line = Line(self.begin, self.end, self.drawContext)
        self.app.objects.append(self.line)
        self.app.repaint()

    def unexecute(self):
        self.app.objects.remove(self.line)
        self.app.repaint()
