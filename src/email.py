import smtplib
import toml
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders
from src.config import load_email_config


def send_mail(send_to, subject, message, files=[]):
    config = load_email_config()
    return _send_mail(
        send_from=config["address"],
        send_to=send_to,
        subject=subject,
        message=message,
        files=files,
        server=config["server"],
        port=config["port"],
        username=config["username"],
        password=config["password"],
        use_tls=config["use_tls"],
    )


def _send_mail(
    send_from,
    send_to,
    subject,
    message,
    files=[],
    server="localhost",
    port=587,
    username="",
    password="",
    use_tls=True,
):
    """Compose and send email with provided info and attachments.

    Args:
        send_from (str): from name
        send_to (list[str]): to name(s)
        subject (str): message title
        message (str): message body
        files (list[str]): list of file paths to be attached to email. Alternatively
        it is possible to pass a list of 2-element tuples with the path and the
        desired filename which will be showed in the mail.
        server (str): mail server host name
        port (int): port number
        username (str): server auth username
        password (str): server auth password
        use_tls (bool): use TLS mode
    """
    assert isinstance(send_to, list)
    assert isinstance(files, list)

    msg = MIMEMultipart()
    msg["From"] = send_from
    msg["To"] = COMMASPACE.join(send_to)
    msg["Date"] = formatdate(localtime=True)
    msg["Subject"] = subject

    msg.attach(MIMEText(message))

    for path in files:
        if isinstance(path, tuple):
            path, filename = path
        else:
            filename = path
        part = MIMEBase("application", "octet-stream")
        with open(path, "rb") as file:
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            'attachment; filename="{}"'.format(Path(filename).name),
        )
        msg.attach(part)

    smtp = smtplib.SMTP(server, port)
    if use_tls:
        smtp.starttls()
    smtp.login(username, password)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.quit()
