import os
import sys
from os.path import join


from PyQt5.QtCore import QUrl
from PyQt5.QtQml import qmlRegisterType
from PyQt5.QtQuick import QQuickView
from PyQt5.QtWidgets import QApplication

from qtypes.argv import ArgParser
from qtypes.vend import Vend


if __name__ == '__main__':
    # Reminder to self, see link for why we avoid a 'main' function here
    # http://pyqt.sourceforge.net/Docs/PyQt5/pyqt4_differences.html#object-destruction-on-exit

    app = QApplication(sys.argv)
    print(sys.version)
    print("InvoiceIt")
    root = os.path.dirname(__file__)

    app.setApplicationName("InvoiceIt")
    app.setApplicationDisplayName("InvoiceIt")
    app.setApplicationVersion("0.1")

    view = QQuickView()
    qmlRegisterType(ArgParser, "ArgV", 1, 0, "ArgParser")
    qmlRegisterType(Vend, "Vend", 1, 0, "Vendor")

    f = QUrl.fromLocalFile(join(root, 'qml', 'main.qml'))
    view.setResizeMode(QQuickView.SizeRootObjectToView)
    view.setSource(f)
    view.show()

    sys.exit(app.exec_())
