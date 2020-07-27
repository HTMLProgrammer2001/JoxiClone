from Classes.States.Edit.EditLineState import EditLineState
from Classes.Toolbars.ObjectToolbars.ArrowToolbar import ArrowToolbar
from Intefaces.IToolbar import IToolbar


class EditArrowState(EditLineState):
    def getToolbar(self) -> IToolbar:
        return ArrowToolbar()
