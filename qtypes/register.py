import os

from PyQt5.QtCore import QUrl, pyqtSlot, pyqtSignal, pyqtProperty
from PyQt5.QtQuick import QQuickItem


class Register(QQuickItem):

    registerChanged = pyqtSignal(str)

    def __init__(self, cache, parent=None):
        super(Register, self).__init__(parent)
        self._cache = cache
        self._cfg = None
        return

    @pyqtSlot(str)
    def setRegister(self, registerID):
        self._cfg = self._cache.get_config(registerID)
        self.registerChanged.emit(self.id)
        return

    @pyqtSlot(str, QUrl, str, str, str, str, str, str, str, str, str, int, str, str, str, str, str, result=bool)
    def save(self, registerID, imgSrc, taxID, tradingName, legalName,
             postalAddress, physicalAddress, email, emailSrv, emailUsr,
             emailPwd, port, security, landline, mobile,
             paymentInstructions, footerMessage):

        if not self._cfg:
            print('No RegisterConfig selected!!!')
            return False
        elif registerID != self._cfg.id:
            print('Register ID mismatch!!!')
            return False

        cfg = self._cfg

        if os.name == 'posix':
            cfg.logo_path_posix = imgSrc.toString()
        elif os.name == 'nt':
            cfg.logo_path_win = imgSrc.toString()

        cfg.trading_name = tradingName
        cfg.legal_name = legalName
        cfg.postal_address = postalAddress
        cfg.physical_address = physicalAddress
        cfg.email = email
        cfg.email_server = emailSrv
        cfg.email_user = emailUsr
        cfg.email_password = emailPwd
        cfg.email_port = port
        cfg.email_secure_method = security
        cfg.landline_ph = landline
        cfg.mobile_ph = mobile
        cfg.tax_id = taxID
        cfg.payment_instructions = paymentInstructions
        cfg.footer_message = footerMessage

        self._cache.session.commit()
        self.registerChanged.emit(self.id)
        print('RegisterConfig successfully saved :)')
        return True

    @pyqtProperty(str, notify=registerChanged)
    def id(self):
        if not self._cfg:
            return ""
        return self._cfg.id

    @pyqtProperty(QUrl, notify=registerChanged)
    def logoPath(self):
        if not self._cfg:
            return QUrl()
        elif os.name == 'posix':    # linux, macos
            return QUrl(self._cfg.logo_path_posix)
        elif os.name == 'nt':       # windows
            return QUrl(self._cfg.logo_path_win)
        return QUrl(self._cfg.logo_path_posix)

    @pyqtProperty(str, notify=registerChanged)
    def tradingName(self):
        if not self._cfg:
            return ""
        return self._cfg.trading_name

    @pyqtProperty(str, notify=registerChanged)
    def legalName(self):
        if not self._cfg:
            return ""
        return self._cfg.legal_name

    @pyqtProperty(str, notify=registerChanged)
    def postalAddress(self):
        if not self._cfg:
            return ""
        return self._cfg.postal_address

    @pyqtProperty(str, notify=registerChanged)
    def physicalAddress(self):
        if not self._cfg:
            return ""
        return self._cfg.physical_address

    @pyqtProperty(str, notify=registerChanged)
    def email(self):
        if not self._cfg:
            return ""
        return self._cfg.email

    @pyqtProperty(str, notify=registerChanged)
    def emailServer(self):
        if not self._cfg:
            return ""
        return self._cfg.email_server

    @pyqtProperty(str, notify=registerChanged)
    def emailUser(self):
        if not self._cfg:
            return ""
        return self._cfg.email_user

    @pyqtProperty(str, notify=registerChanged)
    def emailPassword(self):
        if not self._cfg:
            return ""
        return self._cfg.email_password

    @pyqtProperty(int, notify=registerChanged)
    def emailPort(self):
        if not self._cfg:
            return 0
        return self._cfg.email_port

    @pyqtProperty(str, notify=registerChanged)
    def emailSecurity(self):
        if not self._cfg:
            return ""
        return self._cfg.email_secure_method

    @pyqtProperty(str, notify=registerChanged)
    def phoneLandline(self):
        if not self._cfg:
            return ""
        return self._cfg.landline_ph

    @pyqtProperty(str, notify=registerChanged)
    def phoneMobile(self):
        if not self._cfg:
            return ""
        return self._cfg.mobile_ph

    @pyqtProperty(str, notify=registerChanged)
    def taxID(self):
        if not self._cfg:
            return ""
        return self._cfg.tax_id

    @pyqtProperty(str, notify=registerChanged)
    def bankAccount(self):
        if not self._cfg:
            return ""
        return self._cfg.bank_account

    @pyqtProperty(str, notify=registerChanged)
    def paymentInstructions(self):
        if not self._cfg:
            return ""
        return self._cfg.payment_instructions

    @pyqtProperty(str, notify=registerChanged)
    def footerMessage(self):
        if not self._cfg:
            return ""
        return self._cfg.footer_message

    @pyqtProperty(bool, notify=registerChanged)
    def emailAppearsConfigured(self):
        if self._cfg is None:
            return False

        cfg = self._cfg
        isConfigured = (
            cfg.email and
            cfg.email_server and
            cfg.email_user and
            cfg.email_password and
            cfg.email_port)
        return bool(isConfigured)
