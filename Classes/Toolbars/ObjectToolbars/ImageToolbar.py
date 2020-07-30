from PyQt5.QtWidgets import QLabel

from Intefaces.IToolbar import IToolbar


class ImageToolbar(IToolbar):
    def setupUI(self):
        self.addWidget(QLabel('No actions'))

    def setContext(self, context):
        pass

    def getContext(self):
        pass
