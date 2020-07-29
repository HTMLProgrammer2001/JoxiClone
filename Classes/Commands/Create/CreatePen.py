from typing import List
from PyQt5.QtCore import QPoint

from Classes.ObjectData.Pen.Pen import Pen
from Classes.ObjectData.Pen.PenDrawContext import PenDrawContext
from Intefaces.ICommand import ICommand


class CreatePen(ICommand):
    pen: Pen = None

    def __init__(self, app, points: List[QPoint], drawContext: PenDrawContext):
        self.app = app
        self.points = points
        self.drawContext = drawContext

    def execute(self):
        self.pen = Pen(self.points, self.drawContext)
        self.app.objects.append(self.pen)
        self.app.repaint()

    def unexecute(self):
        self.app.objects.remove(self.pen)
        self.app.repaint()
