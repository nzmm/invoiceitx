import argparse
from PyQt5.QtCore import pyqtSlot, QObject


class ArgParser(QObject):

    def __init__(self, parent=None):
        super(ArgParser, self).__init__(parent)
        parser = argparse.ArgumentParser()
        parser.add_argument('-d', '--domain', default="")
        parser.add_argument('-u', '--user', default="")
        parser.add_argument('-p', '--pass', default="")
        parser.add_argument('-o', '--outlet', default="0")
        parser.add_argument('-r', '--register', default="0")
        parser.add_argument('-iv', '--initview', default="login")
        self._args = vars(parser.parse_args())
        return

    @pyqtSlot(str, result=str)
    def getArgument(self, k, fallback=""):
        if k not in self._args:
            return fallback
        return self._args[k]
