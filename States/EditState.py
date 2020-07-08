from PyQt5.QtGui import QPen

from States.IState import IState


class EditState(IState):
    def mouseDown(self, event):
        pass

    def mouseUp(self, event):
        for obj in self.app.objects:
            if obj.contain(event.pos()):
                print('Find:', obj)

    def mouseMove(self, event):
        pass
