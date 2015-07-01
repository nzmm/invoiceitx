from PyQt5.QtCore import pyqtSlot, QObject, QPoint


_view = None
def set_toplevel(view):
    global _view
    _view = view
    return


class AppWindow(QObject):

    def __init__(self, parent=None):
        super(AppWindow, self).__init__(parent)
        global _view
        self._view = _view
        return

    @pyqtSlot(result=QPoint)
    def getCoords(self):
        return QPoint(self._view.x(), self._view.y())
