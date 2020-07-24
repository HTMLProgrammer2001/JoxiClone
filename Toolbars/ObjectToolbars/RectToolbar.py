from Toolbars.IToolbar import IToolbar
from Toolbars.IDrawPrimitiveToolbar import IDrawPrimitiveToolbar
from Context.DrawData.RectDrawContext import RectDrawContext


class RectToolbar(IDrawPrimitiveToolbar, IToolbar):
    def getContext(self):
        return RectDrawContext(self.fill, self.stroke, self.size)

    def setContext(self, context: RectDrawContext):
        self.size = context.width
        self.stroke = context.stroke
        self.fill = context.fill

        self.updateToolbar(False)
