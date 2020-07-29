from PyQt5.QtGui import QPainter, QImage, QColor
from PyQt5.QtWidgets import QWidget


class PaintWidget(QWidget):
    image: QImage = None

    def __init__(self, image, parent=None):
        super().__init__(parent)

        self.image = image

    def paintEvent(self, QPaintEvent):
        qp = QPainter()
        qp.begin(self)
        #qp.fillRect(self.rect(), QColor('white'))
        qp.drawImage(self.rect(), self.image, self.image.rect())
        qp.end()
