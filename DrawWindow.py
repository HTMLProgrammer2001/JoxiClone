from PyQt5 import QtNetwork
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QFileDialog, QMessageBox
from PyQt5.QtGui import QImage, QClipboard, QPixmap, QPainter
from PyQt5.QtCore import Qt, QUrl
import sys
from typing import List
from pickle import dumps, loads
import binascii
import requests

from Classes.Commands.Create.CreateImage import CreateImage
from Classes.Commands.DeleteCommand import DeleteCommand
from Classes.Commands.PasteCommand import PasteCommand
from Classes.History import History
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


class Main(MainDesign):
    contextToolbar = None
    manager = QtNetwork.QNetworkAccessManager()

    def __init__(self, pix: QPixmap = None):
        super().__init__()

        # set image from desktop screen shot
        self.defaultPix = pix

        # connect successfull save handler
        self.manager.finished.connect(self.saveServerFinished)

        # create image
        self.image = QImage(350, 380, QImage.Format_RGB32)
        self.image.fill(Qt.white)

        # settings of GUI
        self.center()
        self.setupUI()
        self.addHandlers()

        # current state of programm
        self.state: IState = LineState(self)

        # history of changes and objects
        self.history = History.getInstance()
        self.objects: List[IObject] = []

    def addHandlers(self):
        self.saveAction.triggered.connect(self.save)
        self.saveBufferAction.triggered.connect(self.saveBuffer)
        self.saveServerAction.triggered.connect(self.saveServer)
        self.clearAction.triggered.connect(self.clear)
        self.unExecuteAction.triggered.connect(self.back)
        self.quitAction.triggered.connect(self.quit)

        self.LineAction.triggered.connect(lambda x: self.setState(LineState(self)))
        self.RectAction.triggered.connect(lambda x: self.setState(RectState(self)))
        self.CircleAction.triggered.connect(lambda x: self.setState(EllipseState(self)))
        self.ArrowAction.triggered.connect(lambda x: self.setState(ArrowState(self)))
        self.PenAction.triggered.connect(lambda x: self.setState(PenState(self)))
        self.PencilAction.triggered.connect(lambda x: self.setState(PencilState(self)))
        self.ImageAction.triggered.connect(lambda x: self.addImage())
        self.TextAction.triggered.connect(lambda x: self.setState(TextState(self)))
        self.EditAction.triggered.connect(lambda x: self.setState(MoveState(self)))

        self.pasteAction.triggered.connect(self.paste)

    def clear(self):
        command = ClearCommand(self)
        command.execute()
        self.history.addCommand(command)
        self.repaint()

    def setToolbar(self, toolbar):
        if self.contextToolbar:
            self.contextToolbar.destroy()
            self.contextToolbar.hide()

        self.contextToolbar = toolbar

        self.addToolBar(Qt.TopToolBarArea, self.contextToolbar)

    def save(self):
        path = QFileDialog().getSaveFileName(self, 'Save image', '', '*.jpg')
        self.image.save(path[0])

    def saveBuffer(self):
        cb: QClipboard = QApplication.clipboard()
        cb.setImage(self.image, mode=cb.Clipboard)

        QMessageBox.information(self, 'Copy', 'Image copied to buffer')

    def saveServer(self):
        name = 'tmp.png'
        url = 'http://localhost:5000/save'

        self.image.save(f"./{name}")

        with open(f"./{name}", 'rb') as img:
            files = {'image': (name, img, 'multipart/form-data', {'Expires': '0'})}

            with requests.Session() as s:
                r = s.post(url, files=files)
                request = r.request
                request.prepare(method="POST", url=url)

                request_qt = QtNetwork.QNetworkRequest(QUrl(url))

                for header, value in request.headers.items():
                    request_qt.setRawHeader(bytes(header, encoding="utf-8"),
                                            bytes(value, encoding="utf-8"))

                self.manager = QtNetwork.QNetworkAccessManager()
                self.manager.finished.connect(self.saveServerFinished)
                self.manager.post(request_qt, request.body)

    def saveServerFinished(self, reply: QtNetwork.QNetworkReply):
        print('Saved')
        print(reply.readAll())

    def back(self):
        self.history.removeCommand()
        self.repaint()

    def setState(self, state: IState):
        if not hasattr(state, 'editField'):
            self.setFocus(Qt.NoFocusReason)

        self.state = state

    def select(self, obj: IObject):
        self.setState(obj.getEditMode(self))

        self.deleteAction.triggered.connect(lambda *args: self.delete(obj))
        self.deleteAction.setDisabled(False)

        self.copyAction.triggered.connect(lambda *args: self.copy(obj))
        self.copyAction.setDisabled(False)

    def unSelect(self):
        self.setState(MoveState(self))
        self.repaint()

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

    def center(self):
        fr = self.frameGeometry()
        qr = QDesktopWidget().availableGeometry().center()

        fr.moveCenter(qr)

        self.move(fr.topLeft())

    def quit(self):
        app.exit()

    def paintEvent(self, *args, **kwargs):
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
    main = Main()

    sys.exit(app.exec_())
