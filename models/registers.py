from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt, QVariant, pyqtSlot


AllRegisters = {
    'id': "all",
    'name': "All Registers"
}


class RegistersModel(QAbstractListModel):

    NameRole = Qt.UserRole + 1
    RegisterIDRole = Qt.UserRole + 2

    _roles = {NameRole: "name",}

    def __init__(self, parent=None):
        super(RegistersModel, self).__init__(parent)
        self._data = []
        return

    def __len__(self):
        return self.rowCount()

    def __getitem__(self, item):
        return self._data[item]

    def __bool__(self):
        return len(self._data) > 0

    def clear(self):
        self.beginResetModel()
        self._data = [AllRegisters,]
        self.endResetModel()
        return

    def addRegister(self, o):
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
            return o['name']

        return QVariant()

    def roleNames(self):
        return self._roles

    @pyqtSlot(int, result=str)
    def getRegisterID(self, index):
        if not self._data:
            return ''
        return self._data[int(index)]['id']

    @pyqtSlot(str, result=int)
    def getIndex(self, registerID):
        if not self._data:
            return -1
        for i, r in enumerate(self._data):
            if r['id'] == registerID:
                return i
        return -1
