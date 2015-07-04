import smtplib

from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders

COMMASPACE = ', '


def _send(smtp, register, from_email, to_email_list, msg):
    try:
        conn = smtp(register.emailServer)
        conn.set_debuglevel(False)
        conn.login(register.emailUser, register.emailPassword)
        try:
            conn.sendmail(from_email, to_email_list, msg.as_string())
        finally:
            conn.close()

    except Exception as e:
        print("PDF send by email failed; %s" % e)
        return False
    return True


def _send_unsecured(*args):
    from smtplib import SMTP
    return _send(SMTP, *args)


def _send_ssl_secured(*args):
    from smtplib import SMTP_SSL
    return _send(SMTP_SSL, *args)

# TODO:
#~ def _send_tls_secured(*args):
    #~ from smtplib import SMTP_SSL
    #~ return _send(SMTP_SSL, *args)


def email_pdfs(register, subject, from_email, to_email_list, text_message='', attachments=[]):
    # TODO: thread
    # Create the container (outer) email message.
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = COMMASPACE.join(to_email_list)

    body = MIMEMultipart('alternative')
    part = MIMEText(text_message, 'plain')
    body.attach(part)
    msg.attach(body)

    for attachment in attachments:
        if attachment['filename'].find('doc') > 0:
            attach_file = MIMEBase('application', 'msword')
        elif attachment['filename'].find('pdf') > 0:
            attach_file = MIMEBase('application', 'pdf')
        else:
            attach_file = MIMEBase('application', 'octet-stream')

        attach_file.set_payload(attachment['data'])
        encoders.encode_base64(attach_file)
        attach_file.add_header('Content-Disposition', 'attachment', filename=attachment['filename'])
        msg.attach(attach_file)

    secured = register.emailSecurity
    r = False
    if not secured or secured == 'None':
        r = _send_unsecured(register, from_email, to_email_list, msg)
    elif secured == 'SSL':
        r = _send_ssl_secured(register, from_email, to_email_list, msg)
    elif secured == 'TLS':
        # TODO: _send_tls_secured(register, from_email, to_email_list, msg)
        raise NotImplementedError('TODO')
    return r
