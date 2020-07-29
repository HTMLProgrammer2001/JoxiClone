from PyQt5.QtGui import QPainter, QImage, QMouseEvent
from PyQt5.QtWidgets import QWidget


class PaintWidget(QWidget):
    def __init__(self, *args):
        super(PaintWidget, self).__init__(*args)

        self.setMouseTracking(True)

    def paintEvent(self, QPaintEvent):
        image = self.parent().image

        qp = QPainter()
        qp.begin(self)
        qp.drawImage(self.rect(), image, image.rect())
        qp.end()

    def mousePressEvent(self, event: QMouseEvent):
        self.parent().state.mouseDown(event)

    def mouseMoveEvent(self, event):
        self.parent().state.mouseMove(event)

    def mouseReleaseEvent(self, event):
        self.parent().state.mouseUp(event)

    def resizeEvent(self, QResizeEvent):
        self.parent().image = QImage(self.width(), self.height(), QImage.Format_RGB32)
        self.repaint()
