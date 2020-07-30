from PyQt5.QtCore import QPoint

from Classes.ObjectData.Text.Text import Text
from Classes.ObjectData.Text.TextDrawContext import TextDrawContext
from Intefaces.ICommand import ICommand


class CreateText(ICommand):
    textObj: Text = None

    def __init__(self, app, pos: QPoint, text: str, drawContext: TextDrawContext):
        self.app = app
        self.pos = pos
        self.text = text
        self.drawContext = drawContext

    def execute(self):
        self.textObj = Text(self.pos, self.text, self.drawContext)
        self.app.objects.append(self.textObj)

    def unexecute(self):
        self.app.objects.remove(self.textObj)
