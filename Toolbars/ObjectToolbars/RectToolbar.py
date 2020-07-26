from Toolbars.IToolbar import IToolbar
from Toolbars.IDrawPrimitiveToolbar import IDrawPrimitiveToolbar
from Context.RectDrawContext import RectDrawContext


class RectToolbar(IDrawPrimitiveToolbar, IToolbar):
    def getContext(self):
        return RectDrawContext(self.fill, self.stroke, self.size)

    def setContext(self, context: RectDrawContext):
        self.sizeComponent.setValue(context.width, notify=False)
        self.strokeComponent.setValue(context.stroke, notify=False)
        self.fillComponent.setValue(context.fill, notify=False)
