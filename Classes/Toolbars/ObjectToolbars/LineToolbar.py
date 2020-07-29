from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtGui import QColor

from Classes.ObjectData.Line.LineDrawContext import LineDrawContext
from Classes.Toolbars.Components.ColorComponent import ColorComponent
from Classes.Toolbars.Components.IComponent import IComponent
from Classes.Toolbars.Components.SizeComponent import SizeComponent
from Intefaces.IMediator import IMediator
from Intefaces.IToolbar import IToolbar


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
        self.sizeComponent = SizeComponent(self, 'Stroke size: ', default=self.size)

    def addColorPicker(self):
        self.colorComponent = ColorComponent(
            self, 'Stroke color: ', default=self.color, transparently=False
        )

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
