from PyQt5.QtGui import QPainter, QImage, QMouseEvent
from PyQt5.QtWidgets import QWidget


class PaintWidget(QWidget):
    def __init__(self, app, *args):
        super(PaintWidget, self).__init__(*args)

        self.app = app

        self.setMouseTracking(True)

    def paintEvent(self, QPaintEvent):
        image = self.app.image

        qp = QPainter()
        qp.begin(self)
        qp.drawImage(self.rect(), image, image.rect())
        qp.end()

    def mousePressEvent(self, event: QMouseEvent):
        self.app.state.mouseDown(event)

    def mouseMoveEvent(self, event):
        self.app.state.mouseMove(event)

    def mouseReleaseEvent(self, event):
        self.app.state.mouseUp(event)

    def resizeEvent(self, QResizeEvent):
        self.app.image = QImage(self.width(), self.height(), QImage.Format_RGB32)
        self.repaint()
