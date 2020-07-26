from Toolbars.IToolbar import IToolbar
from Toolbars.IDrawPrimitiveToolbar import IDrawPrimitiveToolbar
from Context.EllipseDrawContext import EllipseDrawContext


class EllipseToolbar(IDrawPrimitiveToolbar, IToolbar):
    def getContext(self):
        return EllipseDrawContext(self.fill, self.stroke, self.size)

    def setContext(self, context: EllipseDrawContext):
        self.sizeComponent.setValue(context.width, notify=False)
        self.strokeComponent.setValue(context.stroke, notify=False)
        self.fillComponent.setValue(context.fill, notify=False)
