from PyQt5.QtGui import QCursor, QFont
from PyQt5.QtWidgets import QLabel, QFontDialog
from PyQt5.Qt import Qt

from Classes.Toolbars.Components.IComponent import IComponent
from Intefaces.IMediator import IMediator


class FontComponent(IComponent):
    val: QFont = None

    def __init__(self, mediator: IMediator, text: str = 'Color', default=QFont('Arial', 12)):
        self.val = default
        self.text = text

        super().__init__(mediator)

    def drawUI(self):
        self.fontLabel = QLabel()
        self.fontLabel.setText(self.val.toString())
        self.fontLabel.adjustSize()
        self.fontLabel.setCursor(QCursor(Qt.PointingHandCursor))

        self.fontLabel.mousePressEvent = self.changeFont

        self.mediator.addWidget(QLabel(self.text))
        self.mediator.addWidget(self.fontLabel)

        self.mediator.addSeparator()

        self.updateComponent()

    def changeFont(self, *args):
        # show color dialog
        font, ok = QFontDialog.getFont()

        if ok:
            self.setValue(font)

    def setValue(self, newValue, notify=True):
        # change value
        self.val = newValue
        self.changedValue(newValue, notify)

        self.updateComponent()

    def updateComponent(self):
        self.fontLabel.setText(self.val.toString())
