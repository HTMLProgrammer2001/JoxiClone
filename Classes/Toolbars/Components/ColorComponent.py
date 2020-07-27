from PyQt5.QtGui import QColor, QCursor
from PyQt5.QtWidgets import QLabel, QColorDialog
from PyQt5.Qt import Qt

from Classes.Toolbars.Components.IComponent import IComponent
from Intefaces.IMediator import IMediator


class ColorComponent(IComponent):
    def __init__(self, mediator: IMediator, default=QColor('red')):
        self.val = default

        super().__init__(mediator)

    def drawUI(self):
        self.colorLabel = QLabel()
        self.colorLabel.setFixedSize(20, 20)
        self.colorLabel.setCursor(QCursor(Qt.PointingHandCursor))

        # self.transparentColor = QLabel()
        # self.transparentColor.setFixedSize(20, 20)
        # self.transparentColor.setCursor(QCursor(Qt.PointingHandCursor))
        # self.transparentColor.setStyleSheet("border: 1px solid black")
        # self.transparentColor.setToolTip('Transparent')
        #
        # # self.transparentColor.mousePressEvent = self.setTransparent

        self.colorLabel.mousePressEvent = self.changeColor

        self.mediator.addWidget(QLabel('Stroke color: '))
        self.mediator.addWidget(self.colorLabel)
        self.mediator.addSeparator()

        self.updateComponent()

    def changeColor(self, *args):
        color = QColorDialog().getColor(self.val)
        self.setValue(color)

    def setValue(self, newValue, notify=True):
        self.val = newValue
        self.changedValue(newValue, notify)

        self.updateComponent()

    def updateComponent(self):
        self.colorLabel.setStyleSheet(f"background: {self.val.name()}")
