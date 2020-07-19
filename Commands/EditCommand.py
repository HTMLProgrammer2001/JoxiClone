from Commands.ICommand import ICommand
from Objects.IObject import IObject


class EditCommand(ICommand):
    def __init__(self, object: IObject, prevContext, newContext):
        self.object = object
        self.prevContext = prevContext
        self.newContext = newContext

    def execute(self):
        self.object.setContext(self.newContext)

    def unexecute(self):
        self.object.setContext(self.prevContext)
