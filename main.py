from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, QActionGroup, QDesktopWidget, QFileDialog, \
    QToolBar, QWidget, QHBoxLayout, QScrollArea, QMessageBox
from PyQt5.QtGui import QImage, QKeySequence, QClipboard, QPixmap, QPainter, QIcon
from PyQt5.QtCore import Qt
import sys
from typing import List
from pickle import dumps, loads
import binascii

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

from PaintWidget import PaintWidget

from Classes.Toolbars.NoneToolbar import NoneToolbar


class Main(QMainWindow):
    contextToolbar = None

    def __init__(self, pix: QPixmap = None):
        super().__init__()

        self.defaultPix = pix

        self.image = QImage(350, 380, QImage.Format_RGB32)
        self.image.fill(Qt.white)

        self.center()
        self.setupUI()

        self.state: IState = LineState(self)

        self.history = History.getInstance()
        self.objects: List[IObject] = []

    def setupUI(self):
        # setting window
        self.showMaximized()

        centWidget = QWidget(self)
        paintWidget = PaintWidget(self, self)

        vbox = QHBoxLayout()

        vbox.addStretch(1)

        if self.defaultPix:
            paintWidget.setFixedSize(self.defaultPix.size())
        else:
            paintWidget.setFixedSize(500, 500)

        vbox.addWidget(paintWidget)
        vbox.addStretch(1)

        centWidget.setLayout(vbox)

        self.setCentralWidget(centWidget)

        self.setWindowTitle('Paint')

        # create menu
        menu = self.menuBar()
        fileMenu = menu.addMenu('File')

        commandsGroup = QActionGroup(self)

        saveAction = QAction('Save', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.triggered.connect(self.save)
        fileMenu.addAction(saveAction)

        saveBufferAction = QAction('Save to buffer', self)
        saveBufferAction.setShortcut('Ctrl+Shift+S')
        saveBufferAction.triggered.connect(self.saveBuffer)
        fileMenu.addAction(saveBufferAction)

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
        LineAction.setIcon(QIcon('./Images/line.png'))
        LineAction.setCheckable(True)
        LineAction.setChecked(True)
        LineAction.triggered.connect(lambda x: self.setState(LineState(self)))
        commandsGroup.addAction(LineAction)

        RectAction = QAction('Rect', self)
        RectAction.setIcon(QIcon('./Images/rect.png'))
        RectAction.setCheckable(True)
        RectAction.triggered.connect(lambda x: self.setState(RectState(self)))
        commandsGroup.addAction(RectAction)

        CircleAction = QAction('Ellipse', self)
        CircleAction.setIcon(QIcon('./Images/ellipse.png'))
        CircleAction.setCheckable(True)
        CircleAction.triggered.connect(lambda x: self.setState(EllipseState(self)))
        commandsGroup.addAction(CircleAction)

        ArrowAction = QAction('Arrow', self)
        ArrowAction.setCheckable(True)
        ArrowAction.setIcon(QIcon('./Images/arrow.png'))
        ArrowAction.triggered.connect(lambda x: self.setState(ArrowState(self)))
        commandsGroup.addAction(ArrowAction)

        PenAction = QAction('Pen', self)
        PenAction.setIcon(QIcon('./Images/poly.png'))
        PenAction.setCheckable(True)
        PenAction.triggered.connect(lambda x: self.setState(PenState(self)))
        commandsGroup.addAction(PenAction)

        PencilAction = QAction('Pencil', self)
        PencilAction.setCheckable(True)
        PencilAction.setIcon(QIcon('./Images/pencil.png'))
        PencilAction.triggered.connect(lambda x: self.setState(PencilState(self)))
        commandsGroup.addAction(PencilAction)

        ImageAction = QAction('Image', self)
        ImageAction.setCheckable(True)
        ImageAction.setIcon(QIcon('./Images/image.png'))
        ImageAction.triggered.connect(lambda x: self.addImage())
        commandsGroup.addAction(ImageAction)

        TextAction = QAction('Text', self)
        TextAction.setCheckable(True)
        TextAction.setIcon(QIcon('./Images/text.png'))
        TextAction.triggered.connect(lambda x: self.setState(TextState(self)))
        commandsGroup.addAction(TextAction)

        EditAction = QAction('Edit', self)
        EditAction.setCheckable(True)
        EditAction.setIcon(QIcon('./Images/move.png'))
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

        self.setToolbar(NoneToolbar('Context'))
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
