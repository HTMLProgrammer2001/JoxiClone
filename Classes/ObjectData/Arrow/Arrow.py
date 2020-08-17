import math

from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPainter, QPen, QPainterPath

from Classes.ObjectData.Arrow.ArrowDrawContext import ArrowDrawContext
from Classes.ObjectData.Arrow.ArrowMemento import ArrowMemento
from Classes.ObjectData.Line.Line import Line
from Classes.States.Edit.EditArrowState import EditArrowState
from Intefaces.IEditState import IEditState
from Common.helpers import getDistance


class Arrow(Line):
    def __init__(self, begin: QPoint, end: QPoint, drawContext: ArrowDrawContext):
        self.setBegin(begin)
        self.setEnd(end)
        self.setDrawContext(drawContext)

    def draw(self, image):
        width = self.drawContext.width

        qp = QPainter(image)
        qp.setPen(QPen(self.drawContext.stroke, self.drawContext.width))

        # Draw main line
        qp.drawLine(self.getBegin(), self.getEnd())

        # set draw data
        qp.setBrush(self.drawContext.stroke)
        qp.setPen(QPen(self.drawContext.stroke, 0))

        # get vector to end relative begin
        diff = self.getEnd() - self.getBegin()

        # calculate angle between vectors
        try:
            angle = math.acos(diff.x()/getDistance(diff, QPoint(0, 0))) - math.pi/2
        except ZeroDivisionError:
            angle = 0

        # set coord system center to end
        qp.translate(self.getEnd())

        # rotate system in right direction
        if diff.y() < 0:
            qp.rotate(math.degrees(-angle))
        else:
            qp.rotate(math.degrees(math.pi/2 + (math.pi/2 + angle)))

        # translate to draw triangle
        qp.translate(0, -width*math.sqrt(3))

        # draw triangle
        path = QPainterPath()

        path.moveTo(0, 0)
        path.lineTo(-width, width*math.sqrt(3))
        path.lineTo(width, width*math.sqrt(3))
        path.closeSubpath()

        qp.drawPath(path)

    def getMemento(self) -> ArrowMemento:
        return ArrowMemento(self, self.getBegin(), self.getEnd(), self.getDrawContext())

    def getEditMode(self, app) -> IEditState:
        return EditArrowState(app, self)
