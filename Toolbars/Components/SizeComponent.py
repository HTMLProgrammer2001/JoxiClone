from PyQt5.QtWidgets import QSlider, QLabel
from PyQt5.Qt import Qt

from Toolbars.Components.IComponent import IComponent
from Toolbars.IMediator import IMediator


class SizeComponent(IComponent):
    def __init__(self, mediator: IMediator, default=10, min=0, max=50):
        self.min = min
        self.max = max
        self.val = default

        super().__init__(mediator)

    def drawUI(self):
        self.sizeSlider = QSlider()
        self.sizeSlider.setOrientation(Qt.Horizontal)
        self.sizeSlider.setFixedWidth(50)
        self.sizeSlider.setMaximum(self.max)
        self.sizeSlider.setMinimum(self.min)
        self.sizeSlider.setValue(self.val)
        self.sizeSlider.valueChanged[int].connect(self.setValue)
        self.sizeSlider.sliderReleased.connect(lambda: self.changedValue(self.val))

        self.sizeLabel = QLabel()

        self.mediator.addWidget(QLabel('Stroke width: '))
        self.mediator.addWidget(self.sizeSlider)
        self.mediator.addWidget(self.sizeLabel)
        self.mediator.addSeparator()

        self.updateComponent()

    def setValue(self, newValue, notify=True):
        self.val = newValue
        self.changedValue(newValue, notify)

        self.updateComponent()

    def updateComponent(self):
        self.sizeSlider.setValue(self.val)
        self.sizeLabel.setText(f"{self.val}px")
