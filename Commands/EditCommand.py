from Commands.ICommand import ICommand


class EditCommand(ICommand):
    def __init__(self, prevMemento, nextMemento):
        self.prevMemento = prevMemento
        self.nextMemento = nextMemento

    def execute(self):
        self.nextMemento.restore()

    def unexecute(self):
        self.prevMemento.restore()
