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


class IDrawStrokableToolbar(IToolbar, IMediator):
    sizeComponent: IComponent = None
    strokeComponent: IComponent = None

    size = 10
    stroke = QColor('red')

    def setupUI(self):
        self.sizeComponent = SizeComponent(self, 'Stroke width: ', self.size)
        self.strokeComponent = ColorComponent(self, 'Stroke color: ', self.stroke, transparently=False)

    def dispatch(self, comp: IComponent, newValue, notify=True):
        if comp == self.sizeComponent:
            self.size = newValue
        elif comp == self.strokeComponent:
            self.stroke = newValue

        if notify:
            self.notify()

    @abstractmethod
    def getContext(self):
        pass

    @abstractmethod
    def setContext(self, context):
        pass
