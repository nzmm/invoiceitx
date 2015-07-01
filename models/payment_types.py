from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt, QVariant


AllPayments = {
    'id': "-1",
    'name': "All Payment Types",
    'payment_type_id': "all",
}

class PaymentTypesModel(QAbstractListModel):

    IDRole = Qt.UserRole + 1
    NameRole = Qt.UserRole + 2
    TypeIDRole = Qt.UserRole + 3

    _roles = {IDRole: 'payment_id', NameRole: "name", TypeIDRole: 'payment_type_id'}

    def __init__(self, parent=None):
        super(PaymentTypesModel, self).__init__(parent)
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
        self._data = [AllPayments,]
        self.endResetModel()
        return

    def addPaymentType(self, o):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._data.append(o)
        self.endInsertRows()
        return

    def rowCount(self, parent=QModelIndex(), *args, **kwargs):
        return len(self._data)

    def data(self, index, role=Qt.DisplayRole):
        try:
            o = self._data[index.row()]
        except IndexError:
            return QVariant()

        if role == self.IDRole:
            return o['id']
        elif role == self.NameRole:
            return o['name']
        elif role == self.TypeIDRole:
            return o['payment_type_id']

        return QVariant()

    def roleNames(self):
        return self._roles
