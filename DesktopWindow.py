from PyQt5.QtCore import Qt, QPoint, QRect, QObject, pyqtSignal
from PyQt5.QtGui import QPixmap, QPainter, QColor, QKeySequence, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QShortcut


class ScreenShotMaked(QObject):
    event = pyqtSignal(QPixmap)


class DesktopWindow(QMainWindow):
    begin: QPoint = QPoint(0, 0)
    end: QPoint = QPoint(0, 0)
    screenShot: QPixmap = None

    def __init__(self):
        super().__init__()

        self.screenShotSignal = ScreenShotMaked()

        self.takeScreenShot()
        self.addHandlers()
        self.setupUI()

    def takeScreenShot(self):
        self.screenShot = QApplication.primaryScreen().grabWindow(0)

    def addHandlers(self):
        self.exitShortCut = QShortcut('Escape', self)
        self.exitShortCut.activated.connect(lambda *args: self.close())

        self.allShortCut = QShortcut(QKeySequence('Ctrl+A'), self)
        self.allShortCut.activated.connect(self.selectAll)

    def selectAll(self):
        self.begin = QPoint(0, 0)
        self.end = self.rect().bottomRight()

        self.selected()
        self.repaint()

    def selected(self):
        begin = self.begin
        end = self.end

        if begin.x() > end.x():
            begin, end = QPoint(end.x(), begin.y()), QPoint(begin.x(), end.y())

        if begin.y() > end.y():
            begin, end = QPoint(begin.x(), end.y()), QPoint(end.x(), begin.y())

        self.close()
        self.screenShotSignal.event.emit(self.screenShot.copy(QRect(begin, end)))

    def setupUI(self):
        self.setWindowTitle('Joxi')
        self.setWindowIcon(QIcon('./Images/Logo.ico'))
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.showMaximized()

    def paintEvent(self, *args, **kwargs):
        qp = QPainter(self)
        qp.drawPixmap(self.rect(), self.screenShot.copy(self.rect()))
        qp.fillRect(self.rect(), QColor(0, 0, 0, 128))

        begin = self.begin
        end = self.end

        if begin.x() > end.x():
            begin, end = QPoint(end.x(), begin.y()), QPoint(begin.x(), end.y())

        if begin.y() > end.y():
            begin, end = QPoint(begin.x(), end.y()), QPoint(end.x(), begin.y())

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


if __name__ == '__main__':
    app = QApplication([])
    DesktopWindow()

    app.exec_()
