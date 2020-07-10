from typing import List

from Commands.ICommand import ICommand
from Objects.IObject import IObject


class ClearCommand(ICommand):
    deletedObjects: List[IObject] = []

    def execute(self):
        self.deletedObjects = self.app.objects
        self.app.objects = []

    def unexecute(self):
        self.app.objects = self.deletedObjects
