from PyQt5.QtCore import QRect

from Commands.ICommand import ICommand
from Context.RectDrawContext import RectDrawContext
from Objects.Rect import Rect


class CreateRect(ICommand):
    rect: Rect = None

    def __init__(self, app, rect: QRect, drawContext: RectDrawContext):
        self.app = app
        self.rectQ = rect
        self.drawContext = drawContext

    def execute(self):
        self.rect = Rect(self.rectQ, self.drawContext)
        self.app.objects.append(self.rect)
        self.app.repaint()

    def unexecute(self):
        self.app.objects.remove(self.rect)
        self.app.repaint()
