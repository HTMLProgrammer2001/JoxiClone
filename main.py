from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, QActionGroup, QDesktopWidget, QFileDialog
from PyQt5.QtGui import QImage, QPainter, QColor
from PyQt5.QtCore import Qt
import sys
from typing import List, Optional

from history import History
from States.Draw.LineState import LineState
from States.Draw.RectState import RectState
from States.Draw.CircleState import CircleState
from States.MoveState import MoveState
from States.Edit.EditLineState import EditLineState
from States.IState import IState
from Objects.IObject import IObject
from Commands.ClearCommand import ClearCommand


class Main(QMainWindow):
    selected: Optional[IObject] = None

    def __init__(self):
        super().__init__()

        self.center()
        self.setupUI()

        self.image = QImage(500, 500, QImage.Format_RGB32)
        self.image.fill(Qt.white)

        self.brushSize = 3
        self.brushColor = Qt.black
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
        sizeMenu = menu.addMenu('Size')
        brushMenu = menu.addMenu('Brush')
        commandsMenu = menu.addMenu('Commands')

        sizeGroup = QActionGroup(self)
        colorGroup = QActionGroup(self)
        commandsGroup = QActionGroup(self)

        saveAction = QAction('Save', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.triggered.connect(self.save)
        fileMenu.addAction(saveAction)

        clearAction = QAction('Clear', self)
        clearAction.setShortcut('Ctrl+C')
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

        threeAction = QAction('3px', self)
        threeAction.setCheckable(True)
        threeAction.setChecked(True)
        threeAction.setProperty('size', 3)
        threeAction.triggered.connect(self.changeSize)
        sizeGroup.addAction(threeAction)

        fiveAction = QAction('5px', self)
        fiveAction.setCheckable(True)
        fiveAction.triggered.connect(self.changeSize)
        fiveAction.setProperty('size', 5)
        sizeGroup.addAction(fiveAction)

        sevenAction = QAction('7px', self)
        sevenAction.setCheckable(True)
        sevenAction.triggered.connect(self.changeSize)
        sevenAction.setProperty('size', 7)
        sizeGroup.addAction(sevenAction)

        sizeMenu.addActions(sizeGroup.actions())

        blackAction = QAction('Black', self)
        blackAction.setCheckable(True)
        blackAction.setChecked(True)
        blackAction.setProperty('color', 'black')
        blackAction.triggered.connect(self.changeColor)
        colorGroup.addAction(blackAction)

        greenAction = QAction('Green', self)
        greenAction.setCheckable(True)
        greenAction.setProperty('color', 'green')
        greenAction.triggered.connect(self.changeColor)
        colorGroup.addAction(greenAction)

        redAction = QAction('Red', self)
        redAction.setCheckable(True)
        redAction.setProperty('color', 'red')
        redAction.triggered.connect(self.changeColor)
        colorGroup.addAction(redAction)

        brushMenu.addActions(colorGroup.actions())

        LineAction = QAction('Line', self)
        LineAction.setCheckable(True)
        LineAction.setChecked(True)
        LineAction.triggered.connect(lambda x: self.setState(LineState(self)))
        commandsGroup.addAction(LineAction)

        RectAction = QAction('Rect', self)
        RectAction.setCheckable(True)
        RectAction.triggered.connect(lambda x: self.setState(RectState(self)))
        commandsGroup.addAction(RectAction)

        CircleAction = QAction('Cirlce', self)
        CircleAction.setCheckable(True)
        CircleAction.triggered.connect(lambda x: self.setState(CircleState(self)))
        commandsGroup.addAction(CircleAction)

        EditAction = QAction('Edit', self)
        EditAction.setCheckable(True)
        EditAction.triggered.connect(lambda x: self.setState(MoveState(self)))
        commandsGroup.addAction(EditAction)

        commandsMenu.addActions(commandsGroup.actions())

    def clear(self):
        command = ClearCommand(self)
        command.execute()
        self.history.addCommand(command)
        self.repaint()

    def save(self):
        path = QFileDialog().getSaveFileName(self, 'Save image', '', '*.jpg')
        self.image.save(path[0])

    def back(self):
        self.history.removeCommand()
        self.repaint()

    def setState(self, state: IState):
        self.state = state

    def select(self, obj: IObject):
        self.selected = obj
        self.setState(EditLineState(self))

    def unSelect(self):
        self.selected = None
        self.setState(MoveState(self))

    def center(self):
        fr = self.frameGeometry()
        qr = QDesktopWidget().availableGeometry().center()

        fr.moveCenter(qr)

        self.move(fr.topLeft())

    def changeSize(self):
        self.brushSize = self.sender().property('size')

    def changeColor(self):
        self.brushColor = QColor(self.sender().property('color'))

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
