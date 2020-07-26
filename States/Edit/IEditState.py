from abc import abstractmethod

from Commands.EditCommand import EditCommand
from Toolbars.IToolbar import IToolbar
from Toolbars.ToolbarObserver import ToolbarObserver
from States.IState import IState


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

        self.app.deleteAction.triggered.connect(self.delete)
        self.app.deleteAction.setDisabled(False)

    def mouseUp(self, *args):
        if not self.editType:
            return

        if self.editType == 'NO':
            self.app.unSelect()
            return

        self.execChange()

    def execChange(self):
        memento = self.selected.getMemento()

        command = EditCommand(self.curMemento, memento)
        command.execute()

        self.app.history.addCommand(command)
        self.curMemento = memento

    def delete(self):
        print('Delete')

        if self.selected in self.app.objects:
            self.app.objects.remove(self.selected)
            self.app.repaint()

    @abstractmethod
    def getToolbar(self) -> IToolbar:
        pass
