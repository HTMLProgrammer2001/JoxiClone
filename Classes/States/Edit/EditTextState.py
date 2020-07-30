from Classes.ObjectData.Text.TextMemento import TextMemento
from Classes.Toolbars.ObjectToolbars.TextToolbar import TextToolbar
from Intefaces.IEditState import IEditState
from Intefaces.IState import IState
from Intefaces.IToolbar import IToolbar


class EditTextState(IEditState, IState):
    selected = None
    curMemento: TextMemento = None

    def mouseDown(self, event):
        pass

    def mouseMove(self, event):
        pass

    def paint(self, image):
        pass

    def getToolbar(self) -> IToolbar:
        return TextToolbar()
