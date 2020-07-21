from abc import abstractmethod


class ToolbarObserver:
    @abstractmethod
    def changeDraw(self, newDraw):
        pass
