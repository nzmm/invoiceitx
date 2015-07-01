import os
from sqlalchemy import *
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class RegisterConfig(Base):
    __tablename__ = 'register_config'
    id = Column(String, primary_key=True)
    logo_path_win = Column(String)
    logo_path_posix = Column(String)
    trading_name = Column(String)
    legal_name = Column(String)
    postal_address = Column(String)
    physical_address = Column(String)
    email = Column(String)
    landline_ph = Column(String)
    mobile_ph = Column(String)
    tax_id = Column(String)
    bank_account = Column(String)
    payment_instructions = Column(String)
    footer_message = Column(String)
    email_server = Column(String)
    email_user = Column(String)
    email_password = Column(String)
    email_port = Column(Integer, default=25)
    email_secure_method = Column(String, default="None")


class LineNote(Base):
    __tablename__ = 'line_note'
    id = Column(Integer, primary_key=True)
    row = Column(Integer)
    note = Column(String)
    register_sale = Column(String, ForeignKey('register_sale.id'))


class RegisterSale(Base):
    __tablename__ = 'register_sale'
    id = Column(String, primary_key=True)
    customer_name = Column(String)
    customer_email = Column(String)
    line_notes = relationship(LineNote)
    sale_comment = Column(String)
    sent = Column(Boolean, default=False)


class LocalCache(object):

    def __init__(self):
        # db location attrs
        self.db_path = ""

        # engine attrs
        self.db = None
        self.metadata = None
        self.session = None
        return

    def set_domain(self, domain):
        self.db_path = os.path.join(os.getcwd(), 'cache', '%s.db' % domain)
        initially_existed = os.path.exists(self.db_path)
        self.db = create_engine('sqlite:///cache/%s.db' % domain)
        self.db.echo = False
        self.metadata = MetaData(self.db)
        print(self.db_path, initially_existed)
        return

    def init(self, vendor):
        self.set_domain(vendor.domain_name)
        # set up session and orm and create a configured session
        from sqlalchemy.orm import sessionmaker
        session = sessionmaker()
        session.configure(bind=self.db)
        Base.metadata.create_all(self.db)
        self.session = session()
        print('Local cache ready!')
        return

    def get_config(self, register_id):
        if not self.session:
            return None

        try:
            cfg = self.session.query(RegisterConfig).\
                filter(RegisterConfig.id == register_id).one()
        except Exception as e:
            cfg = RegisterConfig(
                id=register_id
            )
            self.session.add(cfg)
            self.session.commit()
        return cfg

    def get_register_sale(self, transaction_id, create=False):
        if not self.session:
            return None

        try:
            rs = self.session.query(RegisterSale).\
                filter(RegisterSale.id == transaction_id).one()
        except Exception as e:
            if not create:
                return None

            rs = RegisterSale(
                id=transaction_id
            )
            self.session.add(rs)
            self.session.commit()
        return rs

    def get_line_note(self, transaction_id, row, create=False):
        if not self.session:
            return None

        try:
            ln = self.session.query(LineNote).\
                filter(LineNote.register_sale == transaction_id).\
                filter(LineNote.row == row).one()
        except Exception as e:
            if not create:
                return None

            ln = LineNote(
                row=row,
                register_sale=transaction_id
            )
            self.session.add(ln)
            self.session.commit()
        return ln
