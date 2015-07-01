import dateutil.parser
from datetime import timedelta
from PyQt5.QtCore import pyqtProperty, pyqtSignal, pyqtSlot, QObject

from vend.local.cache import LocalCache

from vend.vsession import VendAuthSession
from models.outlets import OutletsModel
from models.registers import RegistersModel
from models.sales import RegisterSalesModel

from .sale import SaleDetails
from .register import Register
from .workers import Login, SalesFetcher


class Vend(QObject):

    loggedInStateChanged = pyqtSignal(bool)
    domainChanged = pyqtSignal(str)
    domainChangeComplete = pyqtSignal(str)
    vendInitialised = pyqtSignal()
    jobsChanged = pyqtSignal()

    def __init__(self, parent=None):
        super(Vend, self).__init__(parent)
        self._vendor = VendAuthSession('', '', '')
        self._sessionActive = False
        self._loggedInState = False
        self._authErrorMsg = ""
        self._currentRegister = -1
        self._currentOutlet = 0
        self._cache = LocalCache()
        self._outlets = OutletsModel()
        self._register = Register(self._cache)
        self._registers = RegistersModel()
        self._sales = RegisterSalesModel(self)
        self._saleDetails = SaleDetails(self._register, self._sales, self._cache)
        self.__outlets = []
        self.__registers = []

        # job states
        self._loadingSales = False
        return

    @pyqtProperty(str, notify=domainChanged)
    def domain(self):
        return self._vendor.domain_name

    @pyqtProperty(str, notify=domainChanged)
    def user(self):
        return self._vendor.user

    @pyqtProperty(OutletsModel, notify=loggedInStateChanged)
    def outlets(self):
        return self._outlets

    @pyqtProperty(RegistersModel, notify=loggedInStateChanged)
    def registers(self):
        return self._registers

    @pyqtProperty(int, notify=loggedInStateChanged)
    def loggedIn(self):
        return self._loggedInState

    @pyqtProperty(str, notify=loggedInStateChanged)
    def authError(self):
        return self._authErrorMsg

    @pyqtProperty(bool, notify=jobsChanged)
    def loadingSales(self):
        return self._loadingSales

    def _loginComplete(self, domain, state, err, outlets, registers):
        if state == 200:
            try:
                self.__outlets = outlets['outlets']
            except KeyError:
                self.__outlets = []
            try:
                self.__registers = registers['registers']
            except KeyError:
                self.__registers = []

        self._loggedInState = state
        self._authErrorMsg = err

        self._cache.init(self._vendor)
        self._sessionActive = True

        # outlets
        self._outlets.clear()
        for o in self.__outlets:
            self._outlets.addOutlet(o)

        # registers
        if self._outlets:
            outlet_id = self._outlets[0]['id']
            self._registers.clear()
            for r in self.__registers:
                if r['outlet_id'] == outlet_id:
                    self._registers.addRegister(r)

        self.loggedInStateChanged.emit(state == 200)
        self.domainChangeComplete.emit(domain)
        return

    @pyqtSlot(str, str, str, result=bool)
    def login(self, domain, user, password):
        if not domain or not user or not password:
            self._loggedInState = False
            self._authErrorMsg = "Insufficient arguments"
            self.loggedInStateChanged.emit(False)
            return False

        t = Login(self._vendor, domain, user, password)
        t.events.loginComplete.connect(self._loginComplete)
        t.start()

        self.loggedInStateChanged.emit(False)
        self.domainChanged.emit(domain)
        return True

    @pyqtSlot()
    def logout(self):
        self._vendor.logout()
        print('Logged out of vend account %s' % self._vendor.domain_name)
        self._loggedInState = False
        self._sessionActive = False
        self.__outlets = self.__registers = []
        self.domainChanged.emit(self._vendor.domain_name)
        self.loggedInStateChanged.emit(False)
        return

    def _requestSalesComplete(self, state, err, sales):
        if state == 200:
            self._sales.setSalesData(sales)
            print(state, err, len(sales))
        else:
            print('An error occurred retrieving sales!')

        self._loadingSales = False
        self._sales.rebuildList()
        self.jobsChanged.emit()
        return

    @pyqtSlot(int, str)
    def requestSalesForDate(self, outletIndex, raw_date):
        from_dt = dateutil.parser.parse(raw_date)
        to_dt = from_dt + timedelta(hours=24)

        self._sales.clear()

        # FIXME: dont rely on outlet index value...?
        try:
            outlet_id = self.__outlets[outletIndex]['id']
        except IndexError as e:
            print('Outlet index value too large... will use -1 as fallback')
            outlet_id = self.__outlets[-1]['id']
        except Exception as e:
            print('Err not good, could not select an outlet: %s' % e)
            return

        fetcher = SalesFetcher(
            self._vendor,
            outlet_id,
            from_dt.isoformat(),
            to_dt.isoformat(),
        )
        fetcher.events.requestComplete.connect(self._requestSalesComplete)
        fetcher.start()

        self._loadingSales = True
        self.jobsChanged.emit()
        return

    @pyqtProperty(Register, notify=vendInitialised)
    def register(self):
        return self._register

    @pyqtProperty(RegisterSalesModel, notify=vendInitialised)
    def sales(self):
        return self._sales

    @pyqtProperty(SaleDetails, notify=vendInitialised)
    def saleReceipt(self):
        return self._saleDetails
