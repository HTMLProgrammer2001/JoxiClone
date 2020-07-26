from PyQt5.QtCore import QPoint

from Commands.ICommand import ICommand
from Context.EllipseDrawContext import EllipseDrawContext
from Objects.Ellipse import Ellipse


class CreateEllipse(ICommand):
    ellipse: Ellipse = None

    def __init__(self, app, center: QPoint, radX: int, radY: int, drawContext: EllipseDrawContext):
        self.app = app

        self.center = center
        self.radX = radX
        self.radY = radY
        self.drawContext = drawContext

    def execute(self):
        self.ellipse = Ellipse(self.center, self.radX, self.radY, self.drawContext)
        self.app.objects.append(self.ellipse)
        self.app.repaint()

    def unexecute(self):
        self.app.objects.remove(self.ellipse)
        self.app.repaint()
