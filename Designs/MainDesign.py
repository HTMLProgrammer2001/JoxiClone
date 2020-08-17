from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QActionGroup, QAction, QToolBar, QMainWindow

from Classes.Toolbars.NoneToolbar import NoneToolbar
from PaintWidget import PaintWidget


class MainDesign(QMainWindow):
    def setupUI(self):
        # setting window
        self.showMaximized()

        centWidget = QWidget(self)
        paintWidget = PaintWidget(self, self)

        # setup layout with image on  the center
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

        self.saveAction = QAction('Save', self)
        self.saveAction.setShortcut('Ctrl+S')
        fileMenu.addAction(self.saveAction)

        self.saveBufferAction = QAction('Save to buffer', self)
        self.saveBufferAction.setShortcut('Ctrl+Shift+S')
        fileMenu.addAction(self.saveBufferAction)

        self.saveServerAction = QAction('Save on server', self)
        self.saveServerAction.setShortcut('Ctrl+Alt+S')
        fileMenu.addAction(self.saveServerAction)

        self.clearAction = QAction('Clear', self)
        self.clearAction.setShortcut('Ctrl+F')
        fileMenu.addAction(self.clearAction)

        self.unExecuteAction = QAction('Unexecute', self)
        self.unExecuteAction.setShortcut('Ctrl+Z')
        fileMenu.addAction(self.unExecuteAction)

        self.quitAction = QAction('Quit', self)
        self.quitAction.setShortcut('Ctrl+Q')
        fileMenu.addAction(self.quitAction)

        self.LineAction = QAction('Line', self)
        self.LineAction.setIcon(QIcon('./Images/line.png'))
        self.LineAction.setCheckable(True)
        self.LineAction.setChecked(True)
        commandsGroup.addAction(self.LineAction)

        self.RectAction = QAction('Rect', self)
        self.RectAction.setIcon(QIcon('./Images/rect.png'))
        self.RectAction.setCheckable(True)
        commandsGroup.addAction(self.RectAction)

        self.CircleAction = QAction('Ellipse', self)
        self.CircleAction.setIcon(QIcon('./Images/ellipse.png'))
        self.CircleAction.setCheckable(True)
        commandsGroup.addAction(self.CircleAction)

        self.ArrowAction = QAction('Arrow', self)
        self.ArrowAction.setCheckable(True)
        self.ArrowAction.setIcon(QIcon('./Images/arrow.png'))
        commandsGroup.addAction(self.ArrowAction)

        self.PenAction = QAction('Pen', self)
        self.PenAction.setIcon(QIcon('./Images/poly.png'))
        self.PenAction.setCheckable(True)
        commandsGroup.addAction(self.PenAction)

        self.PencilAction = QAction('Pencil', self)
        self.PencilAction.setCheckable(True)
        self.PencilAction.setIcon(QIcon('./Images/pencil.png'))
        commandsGroup.addAction(self.PencilAction)

        self.ImageAction = QAction('Image', self)
        self.ImageAction.setCheckable(True)
        self.ImageAction.setIcon(QIcon('./Images/image.png'))
        self.ImageAction.triggered.connect(lambda x: self.addImage())
        commandsGroup.addAction(self.ImageAction)

        self.TextAction = QAction('Text', self)
        self.TextAction.setCheckable(True)
        self.TextAction.setIcon(QIcon('./Images/text.png'))
        commandsGroup.addAction(self.TextAction)

        self.EditAction = QAction('Edit', self)
        self.EditAction.setCheckable(True)
        self.EditAction.setIcon(QIcon('./Images/move.png'))
        commandsGroup.addAction(self.EditAction)

        self.deleteAction = QAction('Delete', self)
        self.deleteAction.setDisabled(True)
        self.deleteAction.setShortcut('Delete')

        self.copyAction = QAction('Copy', self)
        self.copyAction.setDisabled(True)
        self.copyAction.setShortcut(QKeySequence('Ctrl+C'))

        self.pasteAction = QAction('Paste', self)
        self.pasteAction.setShortcut(QKeySequence('Ctrl+V'))

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
