from PyQt5.QtWidgets import QLabel, QSlider, QColorDialog
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from PyQt5.QtGui import QColor, QCursor
from abc import abstractmethod

from Toolbars.IToolbar import IToolbar


class ContextChangedSignal(QObject):
    def __init__(self):
        self.signal = pyqtSignal()


class IDrawPrimitiveToolbar(IToolbar):
    size = 10
    stroke = QColor('red')
    fill = QColor('red')

    def setupUI(self):
        self.addSizeSlider()
        self.addStrokePicker()
        self.addFillPicker()

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

        self.addWidget(QLabel('Stroke width: '))
        self.addWidget(self.sizeSlider)
        self.addWidget(self.sizeLabel)
        self.addSeparator()

    def addFillPicker(self):
        self.fillLabel = QLabel()
        self.fillLabel.setFixedSize(20, 20)
        self.fillLabel.setCursor(QCursor(Qt.PointingHandCursor))

        self.fillLabel.mousePressEvent = self.changeFill

        self.addWidget(QLabel('Fill color: '))
        self.addWidget(self.fillLabel)
        self.addSeparator()

    def addStrokePicker(self):
        self.strokeLabel = QLabel()
        self.strokeLabel.setFixedSize(20, 20)
        self.strokeLabel.setCursor(QCursor(Qt.PointingHandCursor))

        self.strokeLabel.mousePressEvent = self.changeStroke

        self.addWidget(QLabel('Stroke color: '))
        self.addWidget(self.strokeLabel)
        self.addSeparator()

    def changeStroke(self, event):
        color = QColorDialog().getColor(self.stroke)
        self.stroke = color

        self.updateToolbar()

    def changeFill(self, event):
        color = QColorDialog().getColor(self.fill)
        self.fill = color

        self.updateToolbar()

    def changeSize(self, val):
        self.size = val

        self.updateToolbar(False)

    def updateToolbar(self, notify=True):
        self.sizeLabel.setText(f"{self.size}px")
        self.fillLabel.setStyleSheet(f"background: {self.fill.name()}")
        self.strokeLabel.setStyleSheet(f"background: {self.stroke.name()}")

        if notify:
            self.notify()

    @abstractmethod
    def getContext(self):
        pass

    @abstractmethod
    def setContext(self, context):
        pass
