import requests
import vend


class VendAuthSession(vend.Vendor):

    def __init__(self, domain, user, password):
        vend.Vendor.__init__(self, domain, user, password)
        self.session = requests.Session()
        return

    def login(self):
        payload = {
            'signin[username]': self.user,
            'signin[password]': self.password
        }
        r = self.session.post('https://%s.vendhq.com/signin' % self.domain_name, data=payload)
        return r

    def logout(self):
        r = self.session.post('https://%s.vendhq.com/signout' % self.domain_name)
        self.user = ""
        self.domain_name = ""
        self.domain = ""
        self.password = ""
        return r

    def get_sales_period(self, *args, **kwargs):
        return vend.RegisterSales.get_sales_period(self, *args, **kwargs)
