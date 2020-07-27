from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, QActionGroup, QDesktopWidget, QFileDialog, \
    QToolBar
from PyQt5.QtGui import QImage, QPainter, QKeySequence, QClipboard
from PyQt5.QtCore import Qt
import sys
from typing import List
from pickle import dumps, loads
import binascii

from Commands.DeleteCommand import DeleteCommand
from Commands.PasteCommand import PasteCommand
from history import History
from States.Draw.LineState import LineState
from States.Draw.RectState import RectState
from States.Draw.EllipseState import EllipseState
from States.MoveState import MoveState
from States.IState import IState
from Objects.IObject import IObject
from Commands.ClearCommand import ClearCommand

from Toolbars.NoneToolbar import NoneToolbar


class Main(QMainWindow):
    def __init__(self):
        super().__init__()

        self.center()
        self.setupUI()

        self.image = QImage(500, 500, QImage.Format_RGB32)
        self.image.fill(Qt.white)

        self.state: IState = LineState(self)

        self.history = History.getInstance()
        self.objects: List[IObject] = []

    def setupUI(self):
        # setting window
        self.resize(500, 500)
        self.show()

        self.setWindowTitle('Paint')

        toolbar = self.addToolBar('Context')

        # create menu
        menu = self.menuBar()
        fileMenu = menu.addMenu('File')

        commandsGroup = QActionGroup(self)

        saveAction = QAction('Save', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.triggered.connect(self.save)
        fileMenu.addAction(saveAction)

        clearAction = QAction('Clear', self)
        clearAction.setShortcut('Ctrl+F')
        clearAction.triggered.connect(self.clear)
        fileMenu.addAction(clearAction)

        unExecuteAction = QAction('Unexecute', self)
        unExecuteAction.setShortcut('Ctrl+Z')
        unExecuteAction.triggered.connect(self.back)
        fileMenu.addAction(unExecuteAction)

        quitAction = QAction('Quit', self)
        quitAction.setShortcut('Ctrl+Q')
        quitAction.triggered.connect(self.quit)
        fileMenu.addAction(quitAction)

        LineAction = QAction('Line', self)
        LineAction.setCheckable(True)
        LineAction.setChecked(True)
        LineAction.triggered.connect(lambda x: self.setState(LineState(self)))
        commandsGroup.addAction(LineAction)

        RectAction = QAction('Rect', self)
        RectAction.setCheckable(True)
        RectAction.triggered.connect(lambda x: self.setState(RectState(self)))
        commandsGroup.addAction(RectAction)

        CircleAction = QAction('Ellipse', self)
        CircleAction.setCheckable(True)
        CircleAction.triggered.connect(lambda x: self.setState(EllipseState(self)))
        commandsGroup.addAction(CircleAction)

        EditAction = QAction('Edit', self)
        EditAction.setCheckable(True)
        EditAction.triggered.connect(lambda x: self.setState(MoveState(self)))
        commandsGroup.addAction(EditAction)

        self.deleteAction = QAction('Delete', self)
        self.deleteAction.setDisabled(True)
        self.deleteAction.setShortcut('Delete')

        self.copyAction = QAction('Copy', self)
        self.copyAction.setDisabled(True)
        self.copyAction.setShortcut(QKeySequence('Ctrl+C'))

        self.pasteAction = QAction('Paste', self)
        self.pasteAction.setShortcut(QKeySequence('Ctrl+V'))
        self.pasteAction.triggered.connect(self.paste)

        menu.addAction(self.deleteAction)
        menu.addAction(self.copyAction)
        menu.addAction(self.pasteAction)

        self.commandsToolbar = QToolBar('Commands')
        self.commandsToolbar.setMovable(False)
        self.commandsToolbar.addActions(commandsGroup.actions())

        self.contextToolbar = NoneToolbar('Context')
        self.contextToolbar.setMovable(False)
        self.contextToolbar.destroy()

        self.addToolBar(Qt.LeftToolBarArea, self.commandsToolbar)
        self.addToolBar(Qt.TopToolBarArea, self.contextToolbar)

    def clear(self):
        command = ClearCommand(self)
        command.execute()
        self.history.addCommand(command)
        self.repaint()

    def setToolbar(self, toolbar):
        self.contextToolbar.destroy()
        self.contextToolbar.hide()

        self.contextToolbar = toolbar

        self.addToolBar(Qt.TopToolBarArea, self.contextToolbar)

    def save(self):
        path = QFileDialog().getSaveFileName(self, 'Save image', '', '*.jpg')
        self.image.save(path[0])

    def back(self):
        self.history.removeCommand()
        self.repaint()

    def setState(self, state: IState):
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
        print('Copy')

    def paste(self):
        try:
            data = binascii.unhexlify(QApplication.clipboard().text())
            obj = loads(data)

            print('Paste')
            command = PasteCommand(self, obj)
            command.execute()

            self.history.addCommand(command)
            self.repaint()
        except binascii.Error:
            pass

    def center(self):
        fr = self.frameGeometry()
        qr = QDesktopWidget().availableGeometry().center()

        fr.moveCenter(qr)

        self.move(fr.topLeft())

    def quit(self):
        app.exit()

    def mousePressEvent(self, event):
        self.state.mouseDown(event)

    def mouseReleaseEvent(self, event):
        self.state.mouseUp(event)

    def mouseMoveEvent(self, event):
        self.state.mouseMove(event)

    def paintEvent(self, *args, **kwargs):
        self.image.fill(Qt.white)

        for obj in self.objects:
            obj.draw(self.image)

        self.state.paint(self.image)

        screenQP = QPainter(self)
        screenQP.drawImage(self.rect(), self.image, self.image.rect())

    def resizeEvent(self, event):
        self.image = QImage(self.width(), self.height(), QImage.Format_RGB32)
        self.repaint()


app = QApplication(sys.argv)
main = Main()

sys.exit(app.exec_())
