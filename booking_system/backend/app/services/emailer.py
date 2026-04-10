import smtplib
from email.mime.text import MIMEText

from ..config import (
    MAIL_FROM,
    SMTP_ENABLED,
    SMTP_HOST,
    SMTP_PASSWORD,
    SMTP_PORT,
    SMTP_TIMEOUT,
    SMTP_USE_SSL,
    SMTP_USE_TLS,
    SMTP_USERNAME,
)


def send_mail(to_addr: str, subject: str, body: str) -> None:
    if not SMTP_ENABLED:
        print(f"[MAIL_DISABLED] to={to_addr} subject={subject}\n{body}\n")
        return

    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = MAIL_FROM
    msg["To"] = to_addr

    smtp_class = smtplib.SMTP_SSL if SMTP_USE_SSL else smtplib.SMTP
    with smtp_class(SMTP_HOST, SMTP_PORT, timeout=SMTP_TIMEOUT) as server:
        if SMTP_USE_TLS and not SMTP_USE_SSL:
            server.starttls()
        if SMTP_USERNAME:
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(MAIL_FROM, [to_addr], msg.as_string())
