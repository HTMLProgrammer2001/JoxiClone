from abc import abstractmethod
from typing import Union

from Toolbars.IMediator import IMediator
from Toolbars.IToolbar import IToolbar


class IComponent:
    mediator: Union[IMediator, IToolbar] = None

    def __init__(self, mediator: IMediator):
        self.mediator = mediator
        self.drawUI()

    def changedValue(self, newValue):
        self.mediator.dispatch(self, newValue)

    @abstractmethod
    def setValue(self, newValue):
        pass

    @abstractmethod
    def drawUI(self):
        pass
