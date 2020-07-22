from Commands.ICommand import ICommand
from Context.ObjectData.EllipseContext import EllipseContext
from Objects.Ellipse import Ellipse


class CreateEllipse(ICommand):
    ellipse: Ellipse = None

    def __init__(self, app, context: EllipseContext):
        self.app = app
        self.context = context

    def execute(self):
        self.ellipse = Ellipse(self.context)
        self.app.objects.append(self.ellipse)
        self.app.repaint()

    def unexecute(self):
        self.app.objects.remove(self.ellipse)
        self.app.repaint()
