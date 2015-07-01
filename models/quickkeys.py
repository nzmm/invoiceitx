from PyQt5.QtCore import pyqtProperty, pyqtSignal, pyqtSlot
from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt, QVariant



class QuickKeysModel(QAbstractListModel):

    NameRole = Qt.UserRole + 1
    ColorRole = Qt.UserRole + 2

    _roles = {
        NameRole: "name",
        ColorRole: "keyColor",}

    def __init__(self, parent=None):
        super(QuickKeysModel, self).__init__(parent)
        self._data = []
        self._name = ""
        return

    def __len__(self):
        return self.rowCount()

    def clear(self):
        self.beginResetModel()
        self._data = []
        self.endResetModel()
        return

    def addQuickKey(self, o):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._data.append(o)
        self.endInsertRows()

    def rowCount(self, parent=QModelIndex(), *args, **kwargs):
        return len(self._data)

    def data(self, index, role=Qt.DisplayRole):
        try:
            o = self._data[index.row()]
        except IndexError:
            return QVariant()

        if role == self.NameRole:
            return o.label
        elif role == self.ColorRole:
            return o.color
        return QVariant()

    def roleNames(self):
        return self._roles



class QuickKeysGroupModel(QAbstractListModel):

    currentKeysChanged = pyqtSignal()

    NameRole = Qt.UserRole + 1

    _roles = {NameRole: "name"}


    def __init__(self, parent=None):
        super(QuickKeysGroupModel, self).__init__(parent)
        self._data = []
        self._curGroup = 0
        self._keys = QuickKeysModel()
        return

    def __len__(self):
        return self.rowCount()

    @pyqtSlot(result=int)
    def length(self):
        return len(self)

    @pyqtSlot(int, result=str)
    def getGroupName(self, i):
        return self._data[i].name

    @pyqtProperty(QuickKeysModel, notify=currentKeysChanged)
    def currentKeys(self):
        return self._keys

    @pyqtSlot(int)
    def setCurrentGroup(self, i):
        self._curGroup = i
        self._keys.clear()
        for k in self._data[i].pages[0].keys:
            self._keys.addQuickKey(k)
        return

    def getKey(self, i):
        return self._keys._data[i]

    def clear(self):
        self.beginResetModel()
        self._curGroup = -1
        self._keys.clear()
        self._data = []
        self.endResetModel()
        return

    def addQuickKeyGroup(self, o):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._data.append(o)
        self.endInsertRows()
        return

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def data(self, index, role=NameRole):
        try:
            o = self._data[index.row()]
        except IndexError:
            return QVariant()

        if role == self.NameRole:
            return o.name
        return QVariant()

    def roleNames(self):
        return self._roles

