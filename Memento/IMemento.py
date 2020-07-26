from abc import abstractmethod

from Objects.IObject import IObject


class IMemento:
    def __init__(self, object: IObject):
        self.object = object

    @abstractmethod
    def restore(self):
        pass
