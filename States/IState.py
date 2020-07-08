from abc import abstractmethod


class IState:
    def __init__(self, app):
        self.app = app

    def mouseDown(self, event):
        pass

    def mouseMove(self, event):
        pass

    def mouseUp(self, event):
        pass
