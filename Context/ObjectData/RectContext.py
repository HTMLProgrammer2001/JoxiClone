from PyQt5.QtCore import QRect

from Context.DrawData.RectDrawContext import RectDrawContext


class RectContext:
    def __init__(self, rect: QRect, draw: RectDrawContext):
        self.rect = rect
        self.draw = draw

    def setRect(self, rect: QRect):
        self.rect = rect

    def setDraw(self, newDraw: RectDrawContext):
        self.draw = newDraw
