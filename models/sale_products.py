from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt, QVariant, pyqtSlot, pyqtSignal, pyqtProperty


class SaleProductsModel(QAbstractListModel):

    SeqnoRole = Qt.UserRole + 1
    NameRole = Qt.UserRole + 2
    QuantityRole = Qt.UserRole + 3
    PriceRole = Qt.UserRole + 4
    TaxRole = Qt.UserRole + 5
    TotalRole = Qt.UserRole + 6
    NoteRole = Qt.UserRole + 7

    _roles = {
        SeqnoRole: "seqno",
        NameRole: "name",
        QuantityRole: "quantity",
        PriceRole: "price",
        TaxRole: "tax",
        TotalRole: "total",
        NoteRole: "note",
    }

    def __init__(self, sale, cache, parent=None):
        super(SaleProductsModel, self).__init__(parent)
        self._sale = sale
        self._cache = cache
        self._data = []
        self._transactionID = ''
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
        self._transactionID = ''
        self.endResetModel()
        return

    def updateProducts(self):
        self.clear()

        products = self._sale['register_sale_products']
        self.beginInsertRows(QModelIndex(), 0, len(products) - 1)
        self._data = products
        self.endInsertRows()
        return

    @pyqtSlot(result=int)
    def rowCount(self, parent=QModelIndex(), *args, **kwargs):
        return len(self._data)

    def data(self, index, role=Qt.DisplayRole):
        try:
            o = self._data[index.row()]
        except IndexError:
            return QVariant()

        if role == self.SeqnoRole:
            return int(index.row())
        elif role == self.NameRole:
            return o['name']
        elif role == self.QuantityRole:
            return o['quantity']
        elif role == self.PriceRole:
            return o['price']
        elif role == self.TaxRole:
            return o['tax']
        elif role == self.TotalRole:
            return round(float(o['price_total']) * (1 + float(o['tax_rate'])), 2)
        elif role == self.NoteRole:
            line_note = self._cache.get_line_note(
                self._sale.transactionID,
                int(index.row()))
            if line_note is None:
                return ""
            return line_note.note
        return QVariant()

    def roleNames(self):
        return self._roles

    @pyqtSlot(int, str)
    def updateLineNote(self, row, note):
        try:
            self._data[row]['line_note'] = note
        except:
            pass
        return

    @pyqtSlot(int, result=str)
    def lineNote(self, row):
        o = self._data[row]
        if 'line_note' in o:
            return o['line_note']
        return ""

    def templateData(self):
        tid = self._sale.transactionID
        cache = self._cache
        data = []
        for row, o in enumerate(self._data):
            line_note = cache.get_line_note(tid, row)
            if line_note is None:
                o['line_note'] = ""
            else:
                o['line_note'] = line_note.note
            data.append(o)
        return data

