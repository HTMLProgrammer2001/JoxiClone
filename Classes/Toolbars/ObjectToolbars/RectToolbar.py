from Intefaces.IToolbar import IToolbar
from Intefaces.IDrawPrimitiveToolbar import IDrawPrimitiveToolbar
from Classes.ObjectData.Rect.RectDrawContext import RectDrawContext


class RectToolbar(IDrawPrimitiveToolbar, IToolbar):
    def getContext(self):
        return RectDrawContext(self.fill, self.stroke, self.size)

    def setContext(self, context: RectDrawContext):
        self.sizeComponent.setValue(context.width, notify=False)
        self.strokeComponent.setValue(context.stroke, notify=False)
        self.fillComponent.setValue(context.fill, notify=False)
