from Toolbars.IToolbar import IToolbar
from Toolbars.IDrawPrimitiveToolbar import IDrawPrimitiveToolbar
from Context.DrawData.EllipseDrawContext import EllipseDrawContext


class EllipseToolbar(IDrawPrimitiveToolbar, IToolbar):
    def getContext(self):
        return EllipseDrawContext(self.fill, self.stroke, self.size)

    def setContext(self, context: EllipseDrawContext):
        self.size = context.width
        self.stroke = context.stroke
        self.fill = context.fill

        self.updateToolbar(False)
