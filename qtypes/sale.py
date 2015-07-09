import os
import sys
import shlex
import subprocess

from PyQt5.QtCore import pyqtSlot, pyqtSignal, pyqtProperty, QUrl
from PyQt5.QtQuick import QQuickItem

from models.sale_products import SaleProductsModel
from models.sale_payments import SalePaymentsModel

from pdf.renderer import render_pdf, DEFAULT_TEMPLATE
from pdf.send import email_pdf_files


class SaleDetails(QQuickItem):

    saleChanged = pyqtSignal()
    saveStateChanged = pyqtSignal()
    detailsInitialised = pyqtSignal()

    def __init__(self, register, sales, cache, parent=None):
        super(SaleDetails, self).__init__(parent)
        self._saving = False
        self._register = register
        self._sales = sales
        self._sale = None
        self._cache = cache
        self._products = SaleProductsModel(self, cache)
        self._payments = SalePaymentsModel(self)
        return

    def __getitem__(self, k):
        if self._sale is None:
            return None
        return self._sale[k]

    @pyqtProperty(str, notify=saleChanged)
    def transactionID(self):
        if self._sale is None:
            return ''
        return self._sale['id']

    @pyqtSlot(int)
    def setSource(self, index):
        self._sale = self._sales[index]
        self._products.updateProducts()
        self._payments.updatePayments()
        self.saleChanged.emit()
        return

    @pyqtSlot(str, str, str, result=bool)
    def saveCustomerDetails(self, name, email, comment):
        sale = self._cache.get_register_sale(
            self.transactionID,
            create=True)

        if sale is None:
            print('No RegisterSale selected!!!')
            return False

        sale.customer_name = name
        sale.customer_email = email
        sale.sale_comment = comment
        self._cache.session.commit()

        print('Customer info successfully saved :)')
        return True

    @pyqtSlot(int, str, result=bool)
    def saveLineNote(self, row, note):
        line_note = self._cache.get_line_note(
            self.transactionID,
            row,
            create=True)

        if line_note is None:
            print('No LineSelected selected!!!')
            return False

        line_note.note = note
        self._cache.session.commit()

        print('LineNote successfully saved :)')
        return True

    @pyqtSlot(result=str)
    def generatePDF(self, show=True):
        r = self._register
        date = '{dt.day} {dt:%B} {dt.year}'.format(dt=self.saleDateTime)
        data = {
            'transaction_id': self.transactionID,
            'brand_image': r.logoPath.toString(),
            'customer_name': self.customerName,
            'customer_email': self.customerEmail,
            'sale_date': date,
            'sale_datetime': self.saleDateTime,
            'invoice_number': self.invoiceNumber,
            'gst_number': r.taxID,
            'legal_entity': r.legalName,
            'trading_name': r.tradingName,
            'postal_address': r.postalAddress,
            'purchase_items': self.saleProducts.templateData(),
            'subtotal': self.subtotal,
            'tax_total': self.taxComponent,
            'tax_name': self.taxName,
            'tax_rate': self.taxRate,
            'total': self.total,
            'payments': self.salePayments.templateData(),
            'amount_due': self.toPay,
            'sale_comment': self.comment,
            'footer_message': r.footerMessage,
            'phone': r.phoneLandline,
            'mobile': r.phoneMobile,
            'email': r.email,
        }

        pdf_dst = render_pdf(
            template=DEFAULT_TEMPLATE,
            data=data,
            show=show)
        return pdf_dst

    @pyqtSlot()
    def emailPDF(self, keep_pdf=False):
        r = self._register
        if not r.email:
            print('Cannot email PDF as you have not configured an email for this register')
            return
        if not self.customerEmail:
            print('Cannot email PDF as a recipient email has not been specified')
            return

        pdf_dst = self.generatePDF(show=False)
        if pdf_dst is None:
            print('Cannot email PDF as PDF generation failed!')
            return

        if self.customerName:
            message = "Hi %s,\n\nHere is your receipt from %s.\n\n" % (self.customerName, r.tradingName)
        else:
            message = "Hi,\n\nHere is your receipt from %s.\n\n" % r.tradingName

        pdfAttachments = [
            {
                'filename': "%s.pdf" % self.invoiceNumber,
                'data': open(pdf_dst, 'rb').read(),
            },
        ]

        email_pdf_files(
            r,
            "Your receipt from %s" % r.tradingName,
            r.email,
            [e.strip() for e in self.customerEmail.split(';')],
            text_message=message,
            attachments=pdfAttachments)

        # mark as sent
        sale = self._cache.get_register_sale(self.transactionID)
        sale.sent = True
        self._cache.session.commit()

        if not keep_pdf:
            try:
                os.remove(pdf_dst)
            except Exception as e:
                print('Could not remove PDF file; %s' % e)

        print('Email sent :D')
        self.saleChanged.emit()
        return

    @pyqtProperty(str, notify=saleChanged)
    def invoiceNumber(self):
        if self._sale is None:
            return "No data"
        return self._sale['invoice_number']

    @pyqtProperty(str, notify=saleChanged)
    def saleDate(self):
        if self._sale is None:
            return "No data"
        return self._sale['sale_date']

    @property
    def saleDateTime(self):
        if self._sale is None:
            return None
        from utilx import toLocalTime
        return toLocalTime(self._sale['sale_date'])

    @pyqtProperty(str, notify=saleChanged)
    def customerAccount(self):
        if self._sale is None:
            return ""
        return self._sale['customer_name']

    @pyqtProperty(str, notify=saleChanged)
    def customerName(self):
        sale = self._cache.get_register_sale(self.transactionID)
        if sale is None:
            return self.customerAccount
        return sale.customer_name or self.customerAccount

    @pyqtProperty(str, notify=saleChanged)
    def customerEmail(self):
        sale = self._cache.get_register_sale(self.transactionID)
        if sale is None:
            return ""
        return sale.customer_email

    @pyqtProperty(str, notify=saleChanged)
    def comment(self):
        sale = self._cache.get_register_sale(self.transactionID)
        if sale is None:
            return ""
        return sale.sale_comment

    @pyqtProperty(SaleProductsModel, notify=detailsInitialised)
    def saleProducts(self):
        return self._products

    @pyqtProperty(SalePaymentsModel, notify=detailsInitialised)
    def salePayments(self):
        return self._payments

    @pyqtProperty(float, notify=saleChanged)
    def total(self):
        if self._sale is None:
            return 0.0
        return float(self._sale['totals']['total_payment'])

    @pyqtProperty(float, notify=saleChanged)
    def taxComponent(self):
        if self._sale is None:
            return 0.0
        return float(self._sale['total_tax'])

    @pyqtProperty(str, notify=saleChanged)
    def taxName(self):
        if self._sale is None:
            return ""
        return self._sale['tax_name']

    @pyqtProperty(float, notify=saleChanged)
    def taxRate(self):
        if self._sale is None:
            return 0.0
        return float(self._sale['taxes'][0]['rate'])

    @pyqtProperty(float, notify=saleChanged)
    def subtotal(self):
        if self._sale is None:
            return 0.0
        return float(self._sale['total_price'])

    @pyqtProperty(float, notify=saleChanged)
    def toPay(self):
        if self._sale is None:
            return 0.0
        return float(self._sale['totals']['total_to_pay'])

    @pyqtProperty(str, notify=saleChanged)
    def note(self):
        if self._sale is None:
            return ""
        return self._sale['note']

    @pyqtProperty(bool, notify=saleChanged)
    def sent(self):
        sale = self._cache.get_register_sale(self.transactionID)
        if sale is None:
            return False
        return sale.sent

    @pyqtProperty(bool, notify=saveStateChanged)
    def saving(self):
        return self._saving
