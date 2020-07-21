from PyQt5.QtCore import QPoint

from Context.DrawData.LineDrawContext import LineDrawContext


class LineContext:
    def __init__(self, begin: QPoint, end: QPoint, draw: LineDrawContext):
        self.draw = draw
        self.begin = begin
        self.end = end

    def setDraw(self, draw: LineDrawContext):
        self.draw = draw

    def setBegin(self, point: QPoint):
        self.begin = point

    def setEnd(self, point: QPoint):
        self.end = point
