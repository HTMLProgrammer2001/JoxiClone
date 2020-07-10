from abc import abstractmethod


class ICommand:
    def __init__(self, app=None):
        self.app = app

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def unexecute(self):
        pass
