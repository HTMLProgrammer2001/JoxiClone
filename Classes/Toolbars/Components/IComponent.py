from abc import abstractmethod
from typing import Union

from Intefaces.IMediator import IMediator
from Intefaces.IToolbar import IToolbar


class IComponent:
    mediator: Union[IMediator, IToolbar] = None

    def __init__(self, mediator: IMediator):
        self.mediator = mediator
        self.drawUI()

    def changedValue(self, newValue, notify=True):
        self.mediator.dispatch(self, newValue, notify)

    @abstractmethod
    def setValue(self, newValue, notify=True):
        pass

    @abstractmethod
    def drawUI(self):
        pass
