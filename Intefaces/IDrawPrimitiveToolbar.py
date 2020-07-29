from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtGui import QColor
from abc import abstractmethod

from Classes.Toolbars.Components.ColorComponent import ColorComponent
from Classes.Toolbars.Components.IComponent import IComponent
from Classes.Toolbars.Components.SizeComponent import SizeComponent
from Intefaces.IMediator import IMediator
from Intefaces.IToolbar import IToolbar


class ContextChangedSignal(QObject):
    def __init__(self):
        self.signal = pyqtSignal()


class IDrawPrimitiveToolbar(IToolbar, IMediator):
    sizeComponent: IComponent = None
    strokeComponent: IComponent = None
    fillComponent: IComponent = None

    size = 10
    stroke = QColor('red')
    fill = QColor('red')

    def setupUI(self):
        self.sizeComponent = SizeComponent(self, 'Stroke width: ', self.size)
        self.strokeComponent = ColorComponent(self, 'Stroke color: ', self.stroke)
        self.fillComponent = ColorComponent(self, 'Fill color: ', self.fill)

    def dispatch(self, comp: IComponent, newValue, notify=True):
        if comp == self.sizeComponent:
            self.size = newValue
        elif comp == self.strokeComponent:
            self.stroke = newValue
        elif comp == self.fillComponent:
            self.fill = newValue

        if notify:
            self.notify()

    @abstractmethod
    def getContext(self):
        pass

    @abstractmethod
    def setContext(self, context):
        pass
