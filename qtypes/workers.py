import threading
from PyQt5.QtCore import pyqtSignal, QObject

import vend


class LoginEvents(QObject):

    progress = pyqtSignal(str)
    loginComplete = pyqtSignal(str, int, str, dict, dict)

    def __init__(self, parent=None):
        QObject.__init__(self, parent)
        return


class FetchSalesEvents(QObject):

    requestComplete = pyqtSignal(int, str, list)

    def __init__(self, parent=None):
        QObject.__init__(self, parent)
        return


class Login(threading.Thread):

    def __init__(self, vendor, domain, user, password):
        threading.Thread.__init__(self, daemon=True)
        self.vendor = vendor
        self.domain = domain
        self.user = user
        self.password = password
        self.events = LoginEvents()
        return

    def _login(self):
        state = 0
        err = ""
        outlets = {}
        registers = {}

        try:
            print('Logging into vend account...')
            self.vendor.set_credentials(self.domain, self.user, self.password)
            r = self.vendor.login()
            state = r.status_code
            if state == 200:
                print('Authentication successful :)')
                print('Fetching vendor outlets...')
                outlets = vend.Outlets.get(self.vendor).json()
                print('Fetching vendor registers...')
                registers = vend.Registers.get(self.vendor).json()
                print('Logged into vend account %s' % self.vendor.domain_name)
            else:
                print('Login failed!!! Status code: %s' % r.status_code)
                err = "HTTP Error %s - Unauthorized" % r.status_code
        except Exception as e:
            print('Login failed!!! Exception: %s' % e)
            err = str(e)

        self.events.loginComplete.emit(self.domain, state, err, outlets, registers)
        return

    def run(self):
        self._login()
        return


class SalesFetcher(threading.Thread):

    def __init__(self, session, outlet_id, sales_from, sales_to):
        threading.Thread.__init__(self, daemon=True)
        self.outlet_id = outlet_id
        self.sales_from = sales_from
        self.sales_to = sales_to
        self.session = session
        self.events = FetchSalesEvents()
        return

    def _fetch(self):
        err = None
        state = 200

        try:
            sales = self.session.get_sales_period(self.outlet_id, self.sales_from, self.sales_to)
        except Exception as e:
            print('Sales fetcher failed!!! Exception: %s' % e)
            sales = None
            err = str(e)
            state = 500

        self.events.requestComplete.emit(state, err, sales)
        return

    def run(self):
        self._fetch()
        return
