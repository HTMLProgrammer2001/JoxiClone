from PyQt5.QtGui import QColor, QCursor
from PyQt5.QtWidgets import QLabel, QColorDialog
from PyQt5.Qt import Qt

from Classes.Toolbars.Components.IComponent import IComponent
from Intefaces.IMediator import IMediator


class ColorComponent(IComponent):
    isTransparent = False
    isTransparently = True

    def __init__(self, mediator: IMediator, text: str = 'Color', default=QColor('red'), transparently=True):
        self.val = default
        self.text = text
        self.isTransparently = transparently

        super().__init__(mediator)

    def drawUI(self):
        self.colorLabel = QLabel()
        self.colorLabel.setFixedSize(20, 20)
        self.colorLabel.setCursor(QCursor(Qt.PointingHandCursor))

        if self.isTransparently:
            self.transparentColor = QLabel()
            self.transparentColor.setFixedSize(30, 20)
            self.transparentColor.setCursor(QCursor(Qt.PointingHandCursor))
            self.transparentColor.setStyleSheet("border: 1px solid black; border-radius: 2px; margin: 0 5px;")
            self.transparentColor.setToolTip('Transparent')

            self.transparentColor.mousePressEvent = self.setTransparent

        self.colorLabel.mousePressEvent = self.changeColor

        self.mediator.addWidget(QLabel(self.text))
        self.mediator.addWidget(self.colorLabel)

        if self.isTransparently:
            self.mediator.addWidget(self.transparentColor)

        self.mediator.addSeparator()

        self.updateComponent()

    def changeColor(self, *args):
        # show color dialog
        color = QColorDialog().getColor(self.val)

        # change mode to non transparent
        self.isTransparent = False

        # change value
        self.setValue(color)

    def setTransparently(self, val: bool):
        self.isTransparently = val

    def setTransparent(self, *args):
        self.setValue(Qt.transparent)
        self.isTransparent = True

    def setValue(self, newValue, notify=True):
        # change mode to transparent if color is transparent
        if newValue == Qt.transparent:
            self.isTransparent = True

        # change value
        self.val = newValue
        self.changedValue(newValue, notify)

        self.updateComponent()

    def updateComponent(self):
        # change styles
        if not self.isTransparent:
            self.colorLabel.setStyleSheet(f"background: {self.val.name()}; border: 1px solid green;")

            if self.isTransparently:
                trStyle = self.transparentColor.styleSheet()
                self.transparentColor.setStyleSheet(trStyle + "border: 1px solid black;")
        else:
            self.colorLabel.setStyleSheet(self.colorLabel.styleSheet() + "border: none;")

            self.transparentColor.setStyleSheet('''
                border: 1px solid green; 
                margin: 0 5px; 
                border-radius: 2px;
            ''')
