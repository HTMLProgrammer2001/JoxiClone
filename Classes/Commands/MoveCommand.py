from PyQt5.QtCore import QPoint

from Intefaces.ICommand import ICommand
from Intefaces.IObject import IObject


class MoveCommand(ICommand):
    def __init__(self, object: IObject, fr: QPoint, to: QPoint):
        self.object = object
        self.fr = fr
        self.to = to

    def execute(self):
        self.object.moveTo(self.to)

    def unexecute(self):
        self.object.moveTo(self.fr)
