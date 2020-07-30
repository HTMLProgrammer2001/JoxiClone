from PyQt5.Qt import QKeyEvent
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLineEdit

from Classes.Commands.Create.CreateText import CreateText
from Classes.ObjectData.Text.Text import Text
from Classes.ObjectData.Text.TextDrawContext import TextDrawContext
from Classes.Toolbars.ObjectToolbars.TextToolbar import TextToolbar
from Intefaces.IState import IState


class TextState(IState):
    begin = None
    isDrawing = False
    editField = None

    def __init__(self, app):
        self.app = app
        self.app.setToolbar(TextToolbar())

        self.editField = QLineEdit(app)
        self.editField.show()
        self.editField.resize(0, 0)
        self.editField.setFocus(Qt.TabFocusReason)
        self.editField.returnPressed.connect(self.execComm)

        self.editField.textChanged[str].connect(self.textChanged)

    def textChanged(self, text):
        self.app.repaint()

    def execComm(self, *args):
        self.isDrawing = False

        textCommand = CreateText(self.app, self.begin, self.editField.text(), self.createContext())
        textCommand.execute()

        self.app.history.addCommand(textCommand)

    def mouseDown(self, event):
        if not self.begin:
            self.begin = event.pos()
            self.isDrawing = True
        else:
            self.isDrawing = False

            textCommand = CreateText(self.app, self.begin, self.editField.text(), self.createContext())
            textCommand.execute()

            self.app.history.addCommand(textCommand)

            self.begin = event.pos()
            self.editField.setText('')

        self.app.repaint()

    def mouseUp(self, event):
        pass

    def mouseMove(self, event: QKeyEvent):
        pass

    def paint(self, image):
        if not self.begin:
            return

        text = Text(self.begin, self.editField.text(), self.createContext())
        text.draw(image)

    def createContext(self) -> TextDrawContext:
        return self.app.contextToolbar.getContext()
