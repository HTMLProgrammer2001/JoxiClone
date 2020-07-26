from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtGui import QColor

from Context.LineDrawContext import LineDrawContext
from Toolbars.Components.ColorComponent import ColorComponent
from Toolbars.Components.IComponent import IComponent
from Toolbars.Components.SizeComponent import SizeComponent
from Toolbars.IMediator import IMediator
from Toolbars.IToolbar import IToolbar


class ContextChangedSignal(QObject):
    def __init__(self):
        self.signal = pyqtSignal()


class LineToolbar(IToolbar, IMediator):
    sizeComponent: IComponent = None
    colorComponent: IComponent = None

    size = 10
    color = QColor('red')

    def setupUI(self):
        self.addSizeSlider()
        self.addColorPicker()

    def addSizeSlider(self):
        self.sizeComponent = SizeComponent(self, default=self.size)

    def addColorPicker(self):
        self.colorComponent = ColorComponent(self, default=self.color)

    def changeSize(self, val):
        self.size = val
        self.notify()

    def getContext(self):
        return LineDrawContext(self.color, self.size)

    def setContext(self, context: LineDrawContext):
        self.sizeComponent.setValue(context.width, notify=False)
        self.colorComponent.setValue(context.stroke, notify=False)

    def dispatch(self, comp: IComponent, newValue, notify=True):
        if comp == self.sizeComponent:
            self.size = newValue
        elif comp == self.colorComponent:
            self.color = newValue

        if notify:
            self.notify()
