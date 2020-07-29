from Classes.ObjectData.Pen.PenDrawContext import PenDrawContext
from Classes.Toolbars.ObjectToolbars.RectToolbar import RectToolbar


class PenToolbar(RectToolbar):
    def getContext(self):
        return PenDrawContext(self.fill, self.stroke, self.size)
