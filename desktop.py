from PyQt5.QtCore import Qt, QPoint, QRect
from PyQt5.QtGui import QPixmap, QPainter, QColor, QKeySequence
from PyQt5.QtWidgets import QApplication, QMainWindow, QShortcut

from main import Main


class MainW(QMainWindow):
    begin: QPoint = QPoint(0, 0)
    end: QPoint = QPoint(0, 0)
    screenShot: QPixmap = None

    def __init__(self):
        super().__init__()

        self.takeScreenShot()
        self.addHandlers()
        self.setupUI()

    def takeScreenShot(self):
        self.screenShot = QApplication.primaryScreen().grabWindow(0)

    def addHandlers(self):
        exitShortCut = QShortcut('Escape', self)
        exitShortCut.activated.connect(lambda *args: app.quit())

        allShortCut = QShortcut(QKeySequence('Ctrl+A'), self)
        allShortCut.activated.connect(self.selectAll)

    def selectAll(self):
        self.begin = QPoint(0, 0)
        self.end = self.rect().bottomRight()

        self.selected()

        self.repaint()

    def selected(self):
        print(1)

        self.close()
        Main(self.screenShot.copy(QRect(self.begin, self.end)))

    def setupUI(self):
        self.resize(300, 300)
        self.setWindowFlag(Qt.FramelessWindowHint)

        self.showMaximized()

    def paintEvent(self, *args, **kwargs):
        qp = QPainter(self)
        qp.drawPixmap(self.rect(), self.screenShot.copy(self.rect()))
        qp.fillRect(self.rect(), QColor(0, 0, 0, 128))

        begin = self.begin
        end = self.end

        pixCopy = self.screenShot.copy(QRect(begin, end))
        qp.drawPixmap(QRect(begin, end), pixCopy)

    def mousePressEvent(self, event):
        if not self.begin:
            self.begin = event.pos()

    def mouseMoveEvent(self, event):
        self.end = event.pos()

        self.repaint()

    def mouseReleaseEvent(self, *args, **kwargs):
        if self.begin:
            self.selected()


app = QApplication([])
m = MainW()

app.exec_()
