from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt, QVariant, pyqtSlot, pyqtSignal, pyqtProperty

from utilx import toLocalTime


class RegisterSalesModel(QAbstractListModel):

    listChanged = pyqtSignal()

    InvoiceNumberRole = Qt.UserRole + 1
    CustomerNameRole = Qt.UserRole + 2
    NotesRole = Qt.UserRole + 3
    SaleDateTimeRole = Qt.UserRole + 4
    SaleTimeRole = Qt.UserRole + 5
    TotalPaymentRole = Qt.UserRole + 6
    RegisterIDRole = Qt.UserRole + 7
    SentRole = Qt.UserRole + 8

    _roles = {
        InvoiceNumberRole: "invoice_number",
        CustomerNameRole: "customer",
        NotesRole: "notes",
        SaleDateTimeRole: "datetime",
        SaleTimeRole: "time",
        TotalPaymentRole: "total_payment",
        RegisterIDRole: "register",
        SentRole: "sent",
    }

    def __init__(self, vend, cache, parent=None):
        super(RegisterSalesModel, self).__init__(parent)
        self._vend = vend
        self._cache = cache
        self.__data = []
        self._data = []

        self._registerFilter = "all"
        self._invoiceFilter = ""
        self._amountFilter = ""
        return

    def __len__(self):
        return self.rowCount()

    def __getitem__(self, item):
        return self._data[item]

    def __bool__(self):
        return len(self._data) > 0

    def clear(self, deep=True):
        self.beginResetModel()
        if deep:
            self.__data = []
        self._data = []
        self.endResetModel()
        self.listChanged.emit()
        return

    def rebuildList(self):
        rF = self._registerFilter
        iF = self._invoiceFilter
        aF = self._amountFilter

        def _filterRegister(s):
            if rF == 'all':
                return True
            return s['register_id'] == rF

        def _filterInvoice(s):
            if iF == '':
                return True
            return iF in s['invoice_number'].lower()

        def _filterAmount(s):
            if aF == '':
                return True
            return float(s['totals']['total_payment']) == float(aF)

        def _filter(s):
            return _filterRegister(s) and _filterInvoice(s) and _filterAmount(s)

        sales = [s for s in self.__data if _filter(s)]
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount() + len(sales) - 1)
        self._data = sales
        self.endInsertRows()
        self.listChanged.emit()
        return

    def rowCount(self, parent=QModelIndex(), *args, **kwargs):
        return len(self._data)

    def data(self, index, role=Qt.DisplayRole):
        try:
            o = self._data[index.row()]
        except IndexError:
            return QVariant()

        if role == self.InvoiceNumberRole:
            return o['invoice_number']
        elif role == self.CustomerNameRole:
            return o['customer_name']
        elif role == self.NotesRole:
            return o['note']
        elif role == self.SaleDateTimeRole:
            dt = toLocalTime(o['sale_date'])
            return dt.isoformat()
        elif role == self.SaleTimeRole:
            dt = toLocalTime(o['sale_date'])
            return dt.time().isoformat()
        elif role == self.TotalPaymentRole:
            return "%.2f" % o['totals']['total_payment']
        elif role == self.RegisterIDRole:
            return o['register_id']
        elif role == self.SentRole:
            sale = self._cache.get_register_sale(o['id'])
            if sale is None:
                return ""
            return bool(sale.sent) and "*" or ""

        return QVariant()

    def roleNames(self):
        return self._roles

    def setSalesData(self, sales):
        self.__data = sales
        print(len(self.__data))
        return

    @pyqtProperty(float, notify=listChanged)
    def displayedSalesValue(self):
        return sum(float(s['totals']['total_payment']) for s in self._data)

    @pyqtSlot(int)
    def setRegisterFilter(self, index):
        registers = self._vend._registers
        if not registers._data:
            return

        registerID = registers._data[index]['id']
        self._registerFilter = registerID

        self.clear(deep=False)
        self.rebuildList()

        self._vend.register.setRegister(registerID)
        return

    @pyqtSlot(str)
    def setInvoiceFilter(self, invoiceNo):
        if not invoiceNo:
            invoiceNumber = ""

        self._invoiceFilter = invoiceNo.strip().lower()

        self.clear(deep=False)
        self.rebuildList()
        return

    @pyqtSlot(str)
    def setAmountFilter(self, amount):
        if not amount:
            amount = ""

        self._amountFilter = amounts
        self.clear(deep=False)
        self.rebuildList()
        return

    @pyqtProperty(int, notify=listChanged)
    def allAvailable(self):
        return len(self.__data)

    @pyqtProperty(int, notify=listChanged)
    def allVisible(self):
        return len(self._data)
