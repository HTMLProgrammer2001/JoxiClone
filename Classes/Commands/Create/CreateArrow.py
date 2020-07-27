from Classes.ObjectData.Arrow.Arrow import Arrow
from Intefaces.ICommand import ICommand
from Classes.ObjectData.Arrow.ArrowDrawContext import ArrowDrawContext


class CreateArrow(ICommand):
    arrow = None

    def __init__(self, app, begin, end, context: ArrowDrawContext):
        self.app = app
        self.begin = begin
        self.end = end
        self.drawContext = context

    def execute(self):
        self.arrow = Arrow(self.begin, self.end, self.drawContext)
        self.app.objects.append(self.arrow)
        self.app.repaint()

    def unexecute(self):
        self.app.objects.remove(self.arrow)
        self.app.repaint()
