from PyQt5.QtCore import QRect

from Intefaces.ICommand import ICommand
from Classes.ObjectData.Rect.RectDrawContext import RectDrawContext
from Classes.ObjectData.Rect.Rect import Rect


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
