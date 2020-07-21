from Commands.ICommand import ICommand
from Context.ObjectData.RectContext import RectContext
from Objects.Rect import Rect


class CreateRect(ICommand):
    rect: Rect = None

    def __init__(self, app, context: RectContext):
        self.app = app
        self.context = context

    def execute(self):
        self.rect = Rect(self.context)
        self.app.objects.append(self.rect)
        self.app.repaint()

    def unexecute(self):
        self.app.objects.remove(self.rect)
        self.app.repaint()
