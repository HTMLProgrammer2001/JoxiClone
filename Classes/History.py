from Intefaces.ICommand import ICommand

from typing import List


class History:
    commands: List[ICommand] = []
    instance = None

    @classmethod
    def getInstance(cls):
        if not cls.instance:
            cls.instance = History()

        return cls.instance

    def addCommand(self, command: ICommand):
        self.commands.append(command)

        print(command.__class__)
        print('Histroy: ', len(self.commands))

    def removeCommand(self):
        if not len(self.commands):
            return

        removed = self.commands.pop()
        removed.unexecute()

        return removed
