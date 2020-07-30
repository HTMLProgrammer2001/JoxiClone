from Classes.ObjectData.Image.ImageMemento import ImageMemento
from Classes.States.Edit.EditRectState import EditRectState
from Classes.Toolbars.ObjectToolbars.ImageToolbar import ImageToolbar
from Intefaces.IToolbar import IToolbar


class EditImageState(EditRectState):
    selected = None
    curMemento: ImageMemento = None

    def getToolbar(self) -> IToolbar:
        return ImageToolbar()
