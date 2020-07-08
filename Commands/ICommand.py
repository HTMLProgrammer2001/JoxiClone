from abc import abstractmethod


class ICommand:
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def unexecute(self):
        pass
