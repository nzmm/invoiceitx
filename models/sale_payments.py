from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt, QVariant, pyqtSlot, pyqtSignal, pyqtProperty


class SalePaymentsModel(QAbstractListModel):

    NameRole = Qt.UserRole + 1
    AmountRole = Qt.UserRole + 2

    _roles = {
        NameRole: "name",
        AmountRole: "amount",
    }

    def __init__(self, sale, parent=None):
        super(SalePaymentsModel, self).__init__(parent)
        self._sale = sale
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

    def updatePayments(self):
        self.clear()

        payments = self._sale['register_sale_payments']
        self.beginInsertRows(QModelIndex(), 0, len(payments) - 1)
        self._data = payments
        self.endInsertRows()
        return

    def rowCount(self, parent=QModelIndex(), *args, **kwargs):
        return len(self._data)

    def data(self, index, role=Qt.DisplayRole):
        try:
            o = self._data[index.row()]
        except IndexError:
            return QVariant()

        if role == self.AmountRole:
            return float(o['amount'])
        elif role == self.NameRole:
            return o['name']
        return QVariant()

    def roleNames(self):
        return self._roles

    def templateData(self):
        return self._data
