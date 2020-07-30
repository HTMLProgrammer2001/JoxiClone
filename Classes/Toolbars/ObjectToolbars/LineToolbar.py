from Classes.ObjectData.Line.LineDrawContext import LineDrawContext
from Intefaces.IDrawStrokableToolbar import IDrawStrokableToolbar


class LineToolbar(IDrawStrokableToolbar):
    def getContext(self):
        return LineDrawContext(self.stroke, self.size)

    def setContext(self, context):
        self.strokeComponent.setValue(context.stroke, notify=False)
        self.sizeComponent.setValue(context.width, notify=False)
