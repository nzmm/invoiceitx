InvoiceIt
=========

Create and send snazzy invoices for Vend sales.  Tested to work on both Windows and Ubuntu Linux.  You need a Vend account for this software to be of any use.


Installation
============

Required software:

* Python 3.4
* PyQt5.4
* wkhtmltopdf
* requests
* python-dateutil
* beautifulsoup4
* SQLAlchemy
* Jinja2


On Windows you'll need to download Python3.4, PyQt5 and wkhtmltopdf from their respective websites and then run their installers.

Using `pip` you can then install the remaining python libs:

```pip install requests python-dateutil beautifulsoup4 SQLAlchemy Jinja2```


On Ubuntu simply use `apt` to install the whole shebang:

```sudo apt install python3.4 python3-pyqt5 wkhtmltopdf python3-requests python3-dateutil python3-bs4 python3-sqlalchemy python3-jinja2```
