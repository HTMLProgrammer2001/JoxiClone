from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.Qt import QKeyEvent
from PyQt5.QtCore import QPoint
from PyQt5.Qt import Qt

from Classes.ObjectData.Line.LineMemento import LineMemento
from Intefaces.IState import IState
from Intefaces.IEditState import IEditState
from Classes.ObjectData.Line.LineDrawContext import LineDrawContext
from Classes.Toolbars.ObjectToolbars.LineToolbar import LineToolbar
from Intefaces.IToolbar import IToolbar
from helpers import getDistance, getBiggerDiff


class EditLineState(IEditState, IState):
    selected = None
    curMemento: LineMemento = None

    def mouseDown(self, event):
        pos = event.pos()
        begin = self.selected.getBegin()
        end = self.selected.getEnd()

        if getDistance(begin, pos) <= 3:
            self.editType = 'BEGIN'
        elif getDistance(end, pos) <= 3:
            self.editType = 'END'
        else:
            self.editType = 'NO'

    def mouseMove(self, event: QKeyEvent):
        if not self.editType:
            return

        begin = self.curMemento.begin
        end = self.curMemento.end

        newPoint: QPoint = event.pos()
        if self.editType == 'BEGIN':
            # Shift pressed
            if event.modifiers() == Qt.ShiftModifier:
                # Parallel to x axis
                if getBiggerDiff(begin, event.pos()) == 'X':
                    newPoint = QPoint(event.pos().x(), end.y())
                else:
                    # Parallel to Y axis
                    newPoint = QPoint(end.x(), event.pos().y())

            self.selected.setBegin(newPoint)

        elif self.editType == 'END':
            # Shift pressed
            if event.modifiers() == Qt.ShiftModifier:
                # Parallel to x axis
                if getBiggerDiff(end, event.pos()) == 'X':
                    newPoint = QPoint(event.pos().x(), begin.y())
                else:
                    # Parallel to y axis
                    newPoint = QPoint(begin.x(), event.pos().y())

            self.selected.setEnd(newPoint)

        self.app.repaint()

    def paint(self, image):
        qp = QPainter(image)

        qp.setPen(QPen(QColor('blue'), 1))

        qp.drawEllipse(self.selected.getBegin(), 3, 3)
        qp.drawEllipse(self.selected.getEnd(), 3, 3)

    def changeDraw(self, newDraw: LineDrawContext):
        self.selected.setDrawContext(newDraw)

        self.execChange()
        self.app.repaint()

    def getToolbar(self) -> IToolbar:
        return LineToolbar()
