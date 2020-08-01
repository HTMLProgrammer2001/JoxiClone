from PyQt5.QtGui import QColor, QFont

from Classes.ObjectData.Text.TextDrawContext import TextDrawContext
from Classes.Toolbars.Components.ColorComponent import ColorComponent
from Classes.Toolbars.Components.FontComponent import FontComponent
from Classes.Toolbars.Components.IComponent import IComponent
from Classes.Toolbars.Components.SizeComponent import SizeComponent
from Intefaces.IMediator import IMediator
from Intefaces.IToolbar import IToolbar


class TextToolbar(IToolbar, IMediator):
    strokeComponent: IComponent = None
    fontComponent: IComponent = None

    stroke = QColor('red')
    font = QFont('Arial', 24)

    def setupUI(self):
        self.strokeComponent = ColorComponent(self, 'Stroke color: ', self.stroke)
        self.fontComponent = FontComponent(self, 'Font: ', self.font)

    def dispatch(self, comp: IComponent, newValue, notify=True):
        if comp == self.strokeComponent:
            self.stroke = newValue
        elif comp == self.fontComponent:
            self.font = newValue

        if notify:
            self.notify()

    def getContext(self):
        return TextDrawContext(self.font, self.stroke)

    def setContext(self, context):
        self.fontComponent.setValue(context.font, notify=False)
        self.strokeComponent.setValue(context.stroke, notify=False)
