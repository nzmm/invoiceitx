import time
import json
import requests

from dateutil import tz, parser
from math import ceil
from os.path import join
from bs4 import BeautifulSoup
from operator import attrgetter

from .utils.dates import tdiff, today, to_date, to_datetime
from utilx import UTC_ZONE

# Vend HTTP API Reference:
# https://developers.vendorhq.com/documentation/api

V1 = '1.0'
REQUEST_PAGE_SIZE = 200
REQUEST_TIMEOUT_SECONDS = 30


class SaleStatus:
    OPEN = 'OPEN'
    CLOSED = 'CLOSED'
    SAVED = 'SAVED'
    LAYBY = 'LAYBY'
    LAYBY_CLOSED = 'LAYBY_CLOSED'
    ONACCOUNT = 'ONACCOUNT'
    ONACCOUNT_CLOSED = 'ONACCOUNT_CLOSED'
    VOIDED = 'VOIDED'


class Vendor(object):

    def __init__(self, domain, usr, pwd):
        self.domain_name = domain
        self.domain = 'https://%s.vendhq.com/api/' % domain
        self.user = usr
        self.password = pwd
        return

    def set_credentials(self, domain, usr, pwd):
        self.domain_name = domain
        self.domain = 'https://%s.vendhq.com/api/' % domain
        self.user = usr
        self.password = pwd
        return

    @property
    def credentials(self):
        return (self.user, self.password)

    def get(self, url, options={}):
        return requests.get(url, auth=self.credentials, params=options, timeout=REQUEST_TIMEOUT_SECONDS)

    def put(self, url, payload={}):
        payload = json.dumps(payload)
        return requests.put(url, auth=self.credentials, data=payload, timeout=REQUEST_TIMEOUT_SECONDS, headers={'Content-Type': 'application/json; charset=utf8'})

    def get_price_books(self, **options):
        url = "https://%s.vendhq.com/price_book" % self.domain_name
        # retrieve the page html
        r = requests.get(url, auth=self.credentials, params=options, timeout=REQUEST_TIMEOUT_SECONDS)
        soup = BeautifulSoup(r.text)
        price_books = []
        for tr in soup.findAll('tr'):
            tds = tr.findAll('td')
            try:
                price_books.append(PriceBook(tds))
            except:
                pass
        return price_books


class Outlets(object):

    FACET_PLURAL = 'outlets'

    @staticmethod
    def get(vendor):
        return vendor.get(join(vendor.domain, Outlets.FACET_PLURAL))


class Registers(object):

    FACET_PLURAL = 'registers'

    @staticmethod
    def get(vendor, **options):
        return vendor.get(join(vendor.domain, Registers.FACET_PLURAL), options)


class PaymentTypes(object):

    FACET_PLURAL = 'payment_types'

    @staticmethod
    def get(vendor, **options):
        return vendor.get(join(vendor.domain, PaymentTypes.FACET_PLURAL), options)


class RegisterSales(object):

    FACET_PLURAL = 'register_sales'

    @staticmethod
    def get(vendor, **options):
        return vendor.get(join(vendor.domain, RegisterSales.FACET_PLURAL), options)

    @staticmethod
    def get_sales_period(vendor, outlet_id, sales_from, sales_to, page_size=REQUEST_PAGE_SIZE):
        # first page options, to retrieve pagination
        options = {
            'since': sales_from,
            'outlet_id': outlet_id,
            'status[]': [SaleStatus.CLOSED, SaleStatus.ONACCOUNT_CLOSED, SaleStatus.LAYBY_CLOSED],
            'page_size': 1
        }

        # get first page and pagination
        sales = RegisterSales.get(vendor, **options).json()
        if 'pagination' in sales:
            n_results = sales['pagination']['results']
        else:
            n_results = len(sales['register_sales'])

        options['page_size'] = page_size
        n_pages = int(ceil(n_results / float(page_size)))
        pages = reversed(range(1, n_pages+1))

        max_dt = parser.parse(sales_to)
        # go through pages in reverse order until we fall outside of the
        # sale_to date
        soi = []
        for page_num in pages:
            options['page'] = page_num
            page = RegisterSales.get(vendor, **options).json()
            dt = parser.parse(page['register_sales'][0]['sale_date'])
            dt = dt.replace(tzinfo=UTC_ZONE)

            if dt > max_dt:
                for s in reversed(page['register_sales']):
                    dt = parser.parse(s['sale_date'])
                    dt = dt.replace(tzinfo=UTC_ZONE)

                    if dt > max_dt:
                        break

                    soi.insert(0, s)
                break
            else:
                soi[0:0] = page['register_sales']

        return soi

    @staticmethod
    def get_sales_value(vendor, outlet_id, sales_from, sales_to, page_size=REQUEST_PAGE_SIZE):
        sales = RegisterSales.get_sales_period(vendor, outlet_id, sales_from, sales_to, page_size)
        value = 0
        for s in sales.register_sales:
            value += float(s.total_price)
        currency = sales.register_sales[0].tax_name.split(' ')[0]
        return currency, value

    @staticmethod
    def get_sales_activity(vendor, outlet_id, sales_from, sales_to, average=True, page_size=REQUEST_PAGE_SIZE):
        sales = RegisterSales.get_sales_period(vendor, outlet_id, sales_from, sales_to, page_size)
        graph = {}
        ttot = stot = 0

        UTC = tz.tzutc()
        NZST = tz.gettz('NZST') # FIXME

        for s in sales.register_sales:
            utc = to_datetime(s.sale_date).replace(tzinfo=UTC)
            nzst = utc.astimezone(NZST)
            hr = nzst.hour
            if nzst.minute >= 30:
                hr += 0.5
            if hr not in graph:
                graph[hr] = [1.0, round(float(s.total_price), 2)]
            else:
                graph[hr][0] += 1.0
                graph[hr][1] = round(graph[hr][1] + float(s.total_price), 2)

            ttot += 1
            stot += float(s.total_price)

        days = max(1, tdiff(sales_from, sales_to).days)
        if average:
            for hr, stats in graph.iteritems():
                graph[hr][0] = round(graph[hr][0] / days, 1)
                graph[hr][1] = round(graph[hr][1] / days, 2)
        graph['day_av'] = [ttot / days, round(stot / days, 2)]
        graph['period'] = [ttot, round(stot, 2)]
        currency = sales.register_sales[0].tax_name.split(' ')[0]
        return currency, graph


class Products(object):

    FACET_SINGULAR = 'product'
    FACET_PLURAL = 'products'

    @staticmethod
    def get(vendor, **options):
        return vendor.get(join(vendor.domain, Products.FACET_PLURAL), options)

    @staticmethod
    def put(vendor, payload):
        r = vendor.put(join(vendor.domain, Products.FACET_PLURAL), payload)
        return r

    @staticmethod
    def get_unique(vendor, product_id):
        return vendor.get(join(vendor.domain, V1, Products.FACET_SINGULAR, product_id))

    @staticmethod
    def get_in_stock(vendor, outlet_id, stock_type, page_size=REQUEST_PAGE_SIZE, incl_negatives=False, progress=False, progress_args=()):
        options = {
            'outlet_id': outlet_id,
            'page_size': page_size
        }

        # get first page and pagination
        prods = Products.get(vendor, **options)
        if prods.has('pagination'):
            n_pages = prods.pagination.pages
            pages = range(1, n_pages+1)

        in_stock = []
        # process remainder of pages
        for page_num in pages:
            if callable(progress):
                progress(int(page_num), int(n_pages), *progress_args)
            options['page'] = page_num
            page = Products.get(vendor, **options)
            for p in page.products:
                if not p.active:
                    continue
                try:
                    count = max(float(o.count) for o in p.inventory if o.outlet_id == outlet_id)
                except:
                    count = 0
                if not incl_negatives:
                    if count > 0 and p.type == stock_type:
                        p.count = count
                        in_stock.append(p)
                else:
                    if count != 0 and p.type == stock_type:
                        p.count = count
                        in_stock.append(p)
            if not page.cached:
                # so we avoid hitting vends' api rate-limits
                time.sleep(0.1)
        return sorted(in_stock, key=attrgetter('name'))

    @staticmethod
    def get_stock(vendor, outlet_id, stock_type="", page_size=REQUEST_PAGE_SIZE, progress=False, progress_args=()):
        options = {
            'outlet_id': outlet_id,
            'page_size': page_size
        }
        in_stock = []

        def _append(p, in_stock):
            if not p.active:
                return False
            if stock_type and p.type == stock_type:
                in_stock.append(p)
            elif not stock_type:
                in_stock.append(p)
            return True

        # get first page and pagination
        prods = Products.get(vendor, **options)
        if prods.has('pagination'):
            n_pages = prods.pagination.pages
            pages = range(1, n_pages+1)

            # process remainder of pages
            for page_num in pages:
                print('Fetching page %s/%s' % (page_num, len(pages)))
                if callable(progress):
                    progress(int(page_num), int(n_pages), *progress_args)
                options['page'] = page_num
                page = Products.get(vendor, **options)
                for p in page.products:
                    _append(p, in_stock)

                if not page.cached:
                    # so we avoid hitting vend's api rate-limits
                    time.sleep(0.1)
        else:
            for p in prods.products:
                _append(p, in_stock)

        return in_stock


class Suppliers(object):

    FACET_SINGULAR = 'supplier'
    FACET_PLURAL = 'suppliers'

    @staticmethod
    def get(vendor, **options):
        return vendor.get(join(vendor.domain, Suppliers.FACET_SINGULAR), options)


class PriceBook(object):
    def __init__(self, tds):
        self.price_book_id = tds[0].find('a')['href'].split('/')[-1]
        self.title = tds[0].text.split('.')[-1]
        self.group = tds[1].text
        self.outlet = tds[2].text
        self.start = tds[3].text
        self.end = tds[4].text
        self.created = tds[5].text
        self.default = tds[6].text == 'View'
        return


