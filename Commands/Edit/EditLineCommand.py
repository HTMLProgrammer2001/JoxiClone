from Commands.ICommand import ICommand
from Context.LineContext import LineContext
from Objects.Line import Line


class EditLineCommand(ICommand):
    def __init__(self, object: Line, prevContext: LineContext, newContext: LineContext):
        self.object = object
        self.prevContext = prevContext
        self.newContext = newContext

    def execute(self):
        self.object.setContext(self.newContext)

    def unexecute(self):
        self.object.setContext(self.prevContext)
