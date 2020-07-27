from PyQt5.QtWidgets import QToolBar
from abc import abstractmethod


class IToolbar(QToolBar):
    observer = None

    def __init__(self, name='Default'):
        super().__init__(name)

        self.setupUI()

    def notify(self):
        if self.observer:
            self.observer.changeDraw(self.getContext())

    def addObserver(self, obs):
        self.observer = obs

    @abstractmethod
    def setupUI(self):
        pass

    @abstractmethod
    def getContext(self):
        pass

    @abstractmethod
    def setContext(self, context):
        pass
