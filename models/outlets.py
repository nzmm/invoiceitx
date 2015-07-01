from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt, QVariant


class OutletsModel(QAbstractListModel):

    NameRole = Qt.UserRole + 1
    OutletIDRole = Qt.UserRole + 2

    _roles = {NameRole: "name", OutletIDRole: "outlet_id"}

    def __init__(self, parent=None):
        super(OutletsModel, self).__init__(parent)
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
        self._data = []
        self.endResetModel()
        return

    def addOutlet(self, o):
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
        elif role == self.OutletIDRole:
            return o['id']

        return QVariant()

    def roleNames(self):
        return self._roles
