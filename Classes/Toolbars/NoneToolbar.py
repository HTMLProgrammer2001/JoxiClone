from PyQt5.QtWidgets import QLabel

from Intefaces.IToolbar import IToolbar


class NoneToolbar(IToolbar):
    def __init__(self, name='Context'):
        super().__init__(name)

        self.setupUI()

    def setupUI(self):
        label = QLabel('No actions')

        self.addWidget(label)

    def getContext(self):
        pass

    def setContext(self, context):
        pass
