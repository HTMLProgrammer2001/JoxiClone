from Classes.ObjectData.Pencil.PencilDrawContext import PencilDrawContext
from Intefaces.IDrawStrokableToolbar import IDrawStrokableToolbar


class PencilToolbar(IDrawStrokableToolbar):
    def getContext(self):
        return PencilDrawContext(self.stroke, self.size)

    def setContext(self, context):
        self.sizeComponent.setValue(context.width)
        self.strokeComponent.setValue(context.stroke)
