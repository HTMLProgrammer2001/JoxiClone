from abc import abstractmethod

from Classes.Commands.EditCommand import EditCommand
from Intefaces.IToolbar import IToolbar
from Intefaces.IToolbarObserver import ToolbarObserver
from Intefaces.IState import IState


class IEditState(IState, ToolbarObserver):
    editType = None
    selected = None
    curMemento = None

    def __init__(self, app, obj):
        super().__init__(app)

        self.app = app
        self.selected = obj
        self.curMemento = obj.getMemento()

        toolbar = self.getToolbar()
        toolbar.addObserver(self)
        toolbar.setContext(self.selected.getDrawContext())

        self.app.setToolbar(toolbar)

    def mouseUp(self, *args):
        if not self.editType:
            return

        if self.editType == 'NO':
            self.app.unSelect()
            return

        self.execChange()

        self.editType = None

    def execChange(self):
        memento = self.selected.getMemento()

        command = EditCommand(self.curMemento, memento)
        command.execute()

        self.app.history.addCommand(command)
        self.curMemento = memento

    def changeDraw(self, newDraw):
        self.selected.setDrawContext(newDraw)

        self.execChange()
        self.app.repaint()

    @abstractmethod
    def getToolbar(self) -> IToolbar:
        pass
