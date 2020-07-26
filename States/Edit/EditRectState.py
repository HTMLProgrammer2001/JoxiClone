from PyQt5.QtCore import QPoint, QRect, Qt
from PyQt5.QtGui import QPainter, QPen, QColor

from Memento.RectMemento import RectMemento
from States.IState import IState
from States.Edit.IEditState import IEditState
from Toolbars.ObjectToolbars.RectToolbar import RectToolbar
from Toolbars.IToolbar import IToolbar
from helpers import getDistance


class EditRectState(IEditState, IState):
    selected = None
    curMemento: RectMemento = None

    def mouseDown(self, event):
        botRight = self.selected.rect.bottomRight()
        topLeft = self.selected.rect.topLeft()

        if getDistance(event.pos(), botRight) <= 3:
            self.editType = 'BOTTOMRIGHT'
        elif getDistance(event.pos(), topLeft) <= 3:
            self.editType = 'TOPLEFT'
        else:
            self.editType = 'NO'

    def mouseMove(self, event):
        if not self.editType:
            return

        rect: QRect = self.selected.getRect()
        endPoint = event.pos()

        if self.editType == 'BOTTOMRIGHT':
            if event.modifiers() & Qt.ShiftModifier:
                diff = rect.bottomRight() - event.pos()
                maxVal = min(diff.x(), diff.y())
                endPoint = QPoint(maxVal, maxVal)

            rect.setBottomRight(endPoint)

        elif self.editType == 'TOPLEFT':
            if event.modifiers() & Qt.ShiftModifier:
                diff = event.pos() - rect.bottomRight()
                minVal = min(diff.x(), diff.y())
                endPoint = QPoint(minVal, minVal)

            rect.setTopLeft(endPoint)

        self.selected.setRect(rect)
        self.app.repaint()

    def paint(self, image):
        qp = QPainter(image)
        qp.setPen(QPen(QColor('blue'), 1))

        qp.drawEllipse(self.selected.rect.bottomRight(), 3, 3)
        qp.drawEllipse(self.selected.rect.topLeft(), 3, 3)

    def changeDraw(self, newDraw):
        self.selected.setDrawContext(newDraw)

        self.execChange()
        self.app.repaint()

    def getToolbar(self) -> IToolbar:
        return RectToolbar()
