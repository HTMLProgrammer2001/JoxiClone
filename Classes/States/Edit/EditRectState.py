from PyQt5.QtCore import QPoint, QRect, Qt
from PyQt5.QtGui import QPainter, QPen, QColor

from Classes.ObjectData.Rect.RectMemento import RectMemento
from Intefaces.IState import IState
from Intefaces.IEditState import IEditState
from Classes.Toolbars.ObjectToolbars.RectToolbar import RectToolbar
from Intefaces.IToolbar import IToolbar
from Common.helpers import getDistance


class EditRectState(IEditState, IState):
    selected = None
    curMemento: RectMemento = None

    def mouseDown(self, event):
        botRight = self.selected.getRect().bottomRight()
        topLeft = self.selected.getRect().topLeft()

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

    def getToolbar(self) -> IToolbar:
        return RectToolbar()
