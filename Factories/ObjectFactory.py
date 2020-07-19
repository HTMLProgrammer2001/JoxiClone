from Context.CircleContext import CircleContext
from Context.RectContext import RectContext
from Context.LineContext import LineContext

from Objects.Circle import Circle
from Objects.Rect import Rect
from Objects.Line import Line


class ObjectFactory:
    @staticmethod
    def createCircle(context: CircleContext):
        return Circle(context)

    @staticmethod
    def createRect(context: RectContext):
        return Rect(context)

    @staticmethod
    def createLine(context: LineContext):
        return Line(context)
