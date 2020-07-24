from copy import copy
from abc import abstractmethod

from Toolbars.IToolbar import IToolbar
from Toolbars.ToolbarObserver import ToolbarObserver
from States.IState import IState


class IEditState(IState, ToolbarObserver):
    editType = None

    def __init__(self, app, obj):
        super().__init__(app)

        self.app = app
        self.selected = obj
        self.curContext = copy(self.selected.context)

        toolbar = self.getToolbar()
        toolbar.addObserver(self)
        toolbar.setContext(self.selected.context.draw)

        self.app.setToolbar(toolbar)

    def mouseUp(self, *args):
        if not self.editType:
            return

        if self.editType == 'NO':
            self.app.unSelect()

        self.execChange()

    @abstractmethod
    def execChange(self):
        pass

    @abstractmethod
    def getToolbar(self) -> IToolbar:
        pass
