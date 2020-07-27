from typing import List

from Intefaces.ICommand import ICommand
from Intefaces.IObject import IObject


class ClearCommand(ICommand):
    deletedObjects: List[IObject] = []

    def execute(self):
        self.deletedObjects = self.app.objects
        self.app.objects = []

    def unexecute(self):
        self.app.objects = self.deletedObjects
