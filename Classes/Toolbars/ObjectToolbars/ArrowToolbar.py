from Classes.ObjectData.Arrow.ArrowDrawContext import ArrowDrawContext
from Classes.Toolbars.ObjectToolbars.LineToolbar import LineToolbar


class ArrowToolbar(LineToolbar):
    def getContext(self):
        return ArrowDrawContext(self.stroke, self.size)
