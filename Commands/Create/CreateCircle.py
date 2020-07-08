from Commands.ICommand import ICommand
from Context.CircleContext import CircleContext
from Objects.Circle import Circle
from history import History


class CreateCircle(ICommand):
    circle: Circle = None

    def __init__(self, app, context: CircleContext):
        self.app = app
        self.context = context

    def execute(self):
        self.circle = Circle(self.context)
        self.app.objects.append(self.circle)
        self.app.repaint()

    def unexecute(self):
        self.app.objects.remove(self.circle)
        self.app.repaint()
