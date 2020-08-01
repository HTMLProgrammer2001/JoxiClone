from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtWidgets import QLineEdit

from Classes.ObjectData.Text.TextMemento import TextMemento
from Classes.Toolbars.ObjectToolbars.TextToolbar import TextToolbar
from Intefaces.IEditState import IEditState
from Intefaces.IState import IState
from Intefaces.IToolbar import IToolbar


class EditTextState(IEditState, IState):
    selected = None
    curMemento: TextMemento = None

    def __init__(self, app, obj):
        super().__init__(app, obj)

        self.editField = QLineEdit(app)
        self.editField.show()
        self.editField.resize(0, 0)
        self.editField.setFocus(Qt.TabFocusReason)
        self.editField.returnPressed.connect(self.execChange)

        self.editField.textChanged[str].connect(self.textChanged)

    def textChanged(self, text):
        self.selected.setText(text)
        self.app.repaint()

    def mouseDown(self, event):
        pass

    def mouseMove(self, event):
        pass

    def paint(self, image):
        qp = QPainter(image)

        qp.setBrush(Qt.transparent)
        qp.setPen(QPen(QColor('blue'), 1))

        qp.drawRect(self.selected.getRect())

    def getToolbar(self) -> IToolbar:
        return TextToolbar()
