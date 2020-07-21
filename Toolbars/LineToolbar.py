from PyQt5.QtWidgets import QLabel, QSlider, QColorDialog
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from PyQt5.QtGui import QColor, QCursor

from Toolbars.IToolbar import IToolbar
from Context.DrawData.LineDrawContext import LineDrawContext


class ContextChangedSignal(QObject):
    def __init__(self):
        self.signal = pyqtSignal()


class LineToolbar(IToolbar):
    size = 10
    color = QColor('red')

    def setupUI(self):
        self.addSizeSlider()
        self.addColorPicker()

        self.updateToolbar()

    def addSizeSlider(self):
        self.sizeSlider = QSlider()
        self.sizeSlider.setOrientation(Qt.Horizontal)
        self.sizeSlider.setFixedWidth(50)
        self.sizeSlider.setMaximum(100)
        self.sizeSlider.setMinimum(0)
        self.sizeSlider.setValue(10)
        self.sizeSlider.valueChanged[int].connect(self.changeSize)
        self.sizeSlider.sliderReleased.connect(self.notify)

        self.sizeLabel = QLabel()

        self.addWidget(self.sizeSlider)
        self.addWidget(self.sizeLabel)
        self.addSeparator()

    def addColorPicker(self):
        self.colorLabel = QLabel()
        self.colorLabel.setFixedSize(20, 20)
        self.colorLabel.setCursor(QCursor(Qt.PointingHandCursor))

        self.colorLabel.mousePressEvent = self.changeColor

        self.addWidget(self.colorLabel)

    def changeColor(self, event):
        color = QColorDialog().getColor(self.color)
        self.color = color

        self.updateToolbar()

    def changeSize(self, val):
        self.size = val

        self.updateToolbar(False)

    def updateToolbar(self, notify=True):
        self.sizeLabel.setText(f"{self.size}px")
        self.colorLabel.setStyleSheet(f"background: {self.color.name()}")

        if notify:
            self.notify()

    def getContext(self):
        return LineDrawContext(self.color, self.size)

    def setContext(self, context: LineDrawContext):
        self.size = context.width
        self.color = context.stroke

        self.updateToolbar(False)
