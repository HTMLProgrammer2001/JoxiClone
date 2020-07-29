from typing import List
from PyQt5.QtCore import QPoint

from Classes.ObjectData.Pencil.Pencil import Pencil
from Classes.ObjectData.Pencil.PencilDrawContext import PencilDrawContext
from Intefaces.ICommand import ICommand


class CreatePencil(ICommand):
    pencil: Pencil = None

    def __init__(self, app, points: List[QPoint], drawContext: PencilDrawContext):
        self.app = app
        self.points = points
        self.drawContext = drawContext

    def execute(self):
        self.pencil = Pencil(self.points, self.drawContext)
        self.app.objects.append(self.pencil)
        self.app.repaint()

    def unexecute(self):
        self.app.objects.remove(self.pencil)
        self.app.repaint()
