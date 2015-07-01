from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt, QVariant


class PriceLevelsModel(QAbstractListModel):

    NameRole = Qt.UserRole + 1
    PriceRole = Qt.UserRole + 2
    TaxRole = Qt.UserRole + 3

    _roles = {NameRole: "name", PriceRole: "price", TaxRole: "tax", }

    def __init__(self, o, parent=None):
        super(PriceLevelsModel, self).__init__(parent)
        self._data = o.get_price_levels()
        print(self._data)
        return

    def __len__(self):
        return self.rowCount()

    def __getitem__(self, item):
        return self._data[item]

    def __bool__(self):
        return len(self._data) > 0

    def rowCount(self, parent=QModelIndex(), *args, **kwargs):
        return len(self._data)

    def data(self, index, role=Qt.DisplayRole):
        try:
            o = self._data[index.row()]
        except IndexError:
            return QVariant()

        print(o)

        if role == self.NameRole:
            return o.name
        elif role == self.PriceRole:
            return o.price
        elif role == self.TaxRole:
            return o.tax

        return QVariant()

    def roleNames(self):
        return self._roles
