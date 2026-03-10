import os
import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

logger = logging.getLogger(__name__)


def send_email(html: str, subject: str) -> None:
    """Send the HTML digest to all recipients via Gmail SMTP."""
    gmail_address = os.environ["GMAIL_ADDRESS"]
    app_password = os.environ["GMAIL_APP_PASSWORD"]
    recipients_raw = os.environ["RECIPIENT_EMAILS"]

    recipients = [r.strip() for r in recipients_raw.split(",") if r.strip()]
    if not recipients:
        raise ValueError("RECIPIENT_EMAILS is empty")

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.ehlo()
        server.starttls()
        server.login(gmail_address, app_password)

        for recipient in recipients:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = gmail_address
            msg["To"] = recipient
            msg.attach(MIMEText(html, "html"))

            try:
                server.sendmail(gmail_address, recipient, msg.as_string())
                logger.info("Sent to %s", recipient)
            except smtplib.SMTPException as e:
                logger.error("Failed to send to %s: %s", recipient, e)
