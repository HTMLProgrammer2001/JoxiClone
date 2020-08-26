from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox
from PyQt5.QtGui import QImage, QClipboard, QPixmap, QPainter, QIcon
from PyQt5.QtCore import Qt
from typing import List
from pickle import dumps, loads
import binascii, sys

from Classes.Commands.Create.CreateImage import CreateImage
from Classes.Commands.DeleteCommand import DeleteCommand
from Classes.Commands.PasteCommand import PasteCommand
from Classes.History import History
from Classes.SaveManager import SaveManager
from Classes.States.Draw.ArrowState import ArrowState
from Classes.States.Draw.LineState import LineState
from Classes.States.Draw.PencilState import PencilState
from Classes.States.Draw.RectState import RectState
from Classes.States.Draw.EllipseState import EllipseState
from Classes.States.Draw.PenState import PenState
from Classes.States.Draw.TextState import TextState
from Classes.States.MoveState import MoveState
from Intefaces.IState import IState
from Intefaces.IObject import IObject
from Classes.Commands.ClearCommand import ClearCommand
from Designs.MainDesign import MainDesign


class DrawWindow(MainDesign):
    contextToolbar = None

    def __init__(self, pix: QPixmap = None):
        super().__init__()

        # set image from desktop screen shot
        self.defaultPix = pix

        self.saveManager = SaveManager(self)

        # create image
        self.image = QImage(350, 380, QImage.Format_RGB32)
        self.image.fill(Qt.white)

        # settings of GUI
        self.setupUI()
        self.addHandlers()

        # current state of programm
        self.state: IState = LineState(self)

        # history of changes and objects
        self.history = History.getInstance()
        self.objects: List[IObject] = []

        self.setWindowIcon(QIcon('./Images/Logo.ico'))
        self.setWindowTitle('Joxi paint')

    def addHandlers(self):
        self.saveAction.triggered.connect(lambda *args: self.saveManager.save(self.image))
        self.saveBufferAction.triggered.connect(lambda *args: self.saveManager.saveBuffer(self.image))
        self.saveServerAction.triggered.connect(lambda *args: self.saveManager.saveServer(self.image))
        self.clearAction.triggered.connect(self.clear)
        self.unExecuteAction.triggered.connect(self.back)
        self.quitAction.triggered.connect(self.quit)

        self.LineAction.triggered.connect(lambda x: self.setState(LineState(self)))
        self.RectAction.triggered.connect(lambda x: self.setState(RectState(self)))
        self.CircleAction.triggered.connect(lambda x: self.setState(EllipseState(self)))
        self.ArrowAction.triggered.connect(lambda x: self.setState(ArrowState(self)))
        self.PenAction.triggered.connect(lambda x: self.setState(PenState(self)))
        self.PencilAction.triggered.connect(lambda x: self.setState(PencilState(self)))
        self.ImageAction.triggered.connect(lambda x: , self.addImage())
        self.TextAction.triggered.connect(lambda x: self.setState(TextState(self)))
        self.EditAction.triggered.connect(lambda x: self.setState(MoveState(self)))

        self.pasteAction.triggered.connect(self.paste)

    def clear(self):
        # clear window
        command = ClearCommand(self)
        command.execute()
        self.history.addCommand(command)
        self.repaint()

    def setToolbar(self, toolbar):
        if self.contextToolbar:
            #delete old toolbar
            self.contextToolbar.destroy()
            self.contextToolbar.hide()

        # set new toolbar
        self.contextToolbar = toolbar
        self.addToolBar(Qt.TopToolBarArea, self.contextToolbar)

    def back(self):
        self.history.removeCommand()
        self.repaint()

    def setState(self, state: IState):
        if not hasattr(state, 'editField'):
            self.setFocus(Qt.NoFocusReason)

        self.state = state

    def select(self, obj: IObject):
        # set edit mode
        self.setState(obj.getEditMode(self))

        # enable actions
        self.deleteAction.triggered.connect(lambda *args: self.delete(obj))
        self.deleteAction.setDisabled(False)

        self.copyAction.triggered.connect(lambda *args: self.copy(obj))
        self.copyAction.setDisabled(False)

    def unSelect(self):
        # set move mode
        self.setState(MoveState(self))
        self.repaint()

        # disable actions
        self.deleteAction.triggered.connect(lambda *args: None)
        self.deleteAction.setDisabled(True)

        self.copyAction.triggered.connect(lambda *args: None)
        self.copyAction.setDisabled(True)

    def delete(self, obj: IObject):
        if obj in self.objects:
            deleteCommand = DeleteCommand(self, obj)
            deleteCommand.execute()

            self.history.addCommand(deleteCommand)
            self.repaint()

    def copy(self, obj: IObject):
        cb: QClipboard = QApplication.clipboard()
        data: str = binascii.hexlify(dumps(obj)).decode('utf-8')

        cb.setText(data, mode=cb.Clipboard)

    def paste(self):
        try:
            data = binascii.unhexlify(QApplication.clipboard().text())
            obj = loads(data)

            command = PasteCommand(self, obj)
            command.execute()

            self.history.addCommand(command)
            self.repaint()
        except binascii.Error:
            pass

    def addImage(self):
        path, f = QFileDialog.getOpenFileName()

        if path:
            imageComm = CreateImage(self, path)
            imageComm.execute()

            self.history.addCommand(imageComm)

    def quit(self):
        app.exit()

    def paintEvent(self, *args, **kwargs):
        # repaint app
        self.image.fill(Qt.white)

        if self.defaultPix:
            qp = QPainter(self.image)
            qp.drawPixmap(self.defaultPix.rect(), self.defaultPix)

            del qp

        for obj in self.objects:
            obj.draw(self.image)

        self.state.paint(self.image)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = DrawWindow()

    sys.exit(app.exec_())
