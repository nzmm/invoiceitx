import os
import sys
import shlex
import subprocess

from os.path import join, dirname


DEFAULT_TEMPLATE = "xeroesque.html"
RENDERED_DIR = join("pdf", "rendered")
RENDERED_TEMPLATE = join(RENDERED_DIR, "receipt.html")
RENDERED_PDF = join(RENDERED_DIR, "receipt.pdf")

from jinja2 import Environment, FileSystemLoader
JENV = Environment(loader=FileSystemLoader(join(dirname(__file__), 'templates')))


# ensure rendered folder exists
if not os.path.exists(RENDERED_DIR):
    os.makedirs(RENDERED_DIR)


# custom filters
def nl2br(s):
    if s is None:
        return s
    return s.replace('\n', '<br>\n')


JENV.filters['nl2br'] = nl2br


def _render_html(template, data):
    # platform specific fonts
    if os.name == 'nt':
        data['fonts'] = "Arial, sans-serif"
    else:
        data['fonts'] = "Ubuntu, Arial, sans-serif"

    # render template
    t = JENV.get_template(template)
    html = t.render(data)
    # save to disk
    f = open(RENDERED_TEMPLATE, "w")
    f.write(html)
    f.close()
    return RENDERED_TEMPLATE


def _render_pdf(html_src, pdf_dst):
    if os.name == 'posix':
        cmds = shlex.split('wkhtmltopdf --page-size a4 %s %s' % (html_src, pdf_dst))
    elif os.name == 'nt':
        wkhtmltopdf = join("C:\\", "Program Files", "wkhtmltopdf", "bin", "wkhtmltopdf.exe")
        if not os.path.isfile(wkhtmltopdf):
            print('wkhtmltopdf does not appear to be installed on your system.')
            print('Please refer to http://wkhtmltopdf.org/downloads.html for download instructions.')
            return 666
        cmds = '"%s" --page-size a4 "%s" "%s"' % (wkhtmltopdf, html_src, pdf_dst)
    return subprocess.check_call(cmds)


def _rm_html(html):
    try:
        os.remove(html)
    except Exception as e:
        print('Could not remove html file... %s' % e)
        return False
    return True


def _show_pdf(pdf_path):
    if sys.platform.startswith('darwin'):   # macos
        subprocess.call(('open', pdf_path))
    elif os.name == 'nt':                   # windows
        os.startfile(pdf_path)
    elif os.name == 'posix':                # linux (and other(?))
        subprocess.call(('xdg-open', pdf_path))
    return


def render_pdf(template=DEFAULT_TEMPLATE, data={}, pdf_dst=RENDERED_PDF, show=False, keep_html=False):
    html = _render_html(template, data)
    r = _render_pdf(html, pdf_dst)
    if r != 0:
        print('Could not generate PDF!!')
        return None

    if not keep_html:
        _rm_html(html)
    if show:
        _show_pdf(pdf_dst)
    return pdf_dst
