from Commands.ICommand import ICommand
from typing import List


class History:
    commands: List[ICommand] = []
    instance = None

    @classmethod
    def getInstance(cls):
        if not cls.instance:
            cls.instance = History()

        return cls.instance

    def addCommand(self, command):
        self.commands.append(command)

    def removeCommand(self):
        if not len(self.commands):
            return

        removed = self.commands.pop()
        removed.unexecute()

        return removed
