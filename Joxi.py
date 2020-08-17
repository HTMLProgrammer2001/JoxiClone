import sys

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow

from Common.treyIcon import SysTrayIcon
from DesktopWindow import DesktopWindow
from DrawWindow import DrawWindow


class Joxi:
    trey = None
    hover_text = 'Joxi'
    window: QMainWindow = None

    def __init__(self):
        self.app = QApplication(sys.argv)

        # create trey menu
        self.menu_options = [('Make screenshot', None, self.makeScreenshot)]
        self.trey = SysTrayIcon('./Images/Logo.ico', self.hover_text, self.menu_options, self.quit)

        # start app execution
        self.app.exec()

    def makeScreenshot(self, *args):
        # show screenshot selecter and subscribe on end
        self.window = DesktopWindow()
        self.window.activateWindow()
        self.window.screenShotSignal.event.connect(self.showPaint)

    def showPaint(self, image: QPixmap):
        self.window = DrawWindow(image)

    def quit(self, *args):
        print('Bye')

        if self.app:
            self.app.exit(0)

        exit(0)


if __name__ == '__main__':
    Joxi()
