from math import sqrt

from PyQt5.QtCore import QPoint, QRect


def getDistance(point: QPoint, point2: QPoint):
    return sqrt((point.x() - point2.x()) ** 2 + (point.y() - point2.y()) ** 2)


def lineContain(point: QPoint, start: QPoint, end: QPoint, width: int):
    return abs(getDistance(start, point) + getDistance(end, point) - getDistance(start, end)) < width


def getBiggerDiff(point: QPoint, point2: QPoint):
    return 'X' if abs(point.x() - point2.x()) > abs(point.y() - point2.y()) else 'Y'


def getEllipseDistance(point: QPoint, center: QPoint, radX: int, radY: int):
    return ((point.x() - center.x())/radX)**2 + ((point.y() - center.y())/radY)


def rectContain(point: QPoint, rect: QRect):
    return rect.left() < point.x() < rect.right() and rect.top() < point.y() < rect.bottom()
