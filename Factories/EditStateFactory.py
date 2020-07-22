from Objects.IObject import IObject
from Objects.Line import Line
from Objects.Rect import Rect
from Objects.Ellipse import Ellipse

from States.Edit.EditRectState import EditRectState
from States.Edit.EditEllipseState import EditEllipseState
from States.Edit.EditLineState import EditLineState


class EditStateFactory:
    @staticmethod
    def getEditState(app, obj: IObject):
        if isinstance(obj, Line):
            return EditLineState(app, obj)
        elif isinstance(obj, Rect):
            return EditRectState(app, obj)
        elif isinstance(obj, Ellipse):
            return EditEllipseState(app, obj)
