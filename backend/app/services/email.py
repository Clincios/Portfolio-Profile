import logging

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

from app.config import get_settings
from app.schemas import ContactCreate

logger = logging.getLogger(__name__)
settings = get_settings()


def _mail_config() -> ConnectionConfig | None:
    if not settings.mail_configured:
        return None
    return ConnectionConfig(
        MAIL_USERNAME=settings.mail_username,
        MAIL_PASSWORD=settings.mail_password,
        MAIL_FROM=settings.mail_from,
        MAIL_PORT=settings.mail_port,
        MAIL_SERVER=settings.mail_server,
        MAIL_STARTTLS=settings.mail_starttls,
        MAIL_SSL_TLS=settings.mail_ssl_tls,
        USE_CREDENTIALS=True,
        VALIDATE_CERTS=True,
    )


async def send_contact_notification(payload: ContactCreate) -> bool:
    """Send email notification for a contact form submission. Returns False if skipped or failed."""
    conf = _mail_config()
    if conf is None:
        logger.info("SMTP not configured; skipping contact email notification.")
        return False

    body = (
        f"New contact form submission\n\n"
        f"Name: {payload.name}\n"
        f"Email: {payload.email}\n"
        f"Subject: {payload.subject}\n\n"
        f"Message:\n{payload.message}\n"
    )
    message = MessageSchema(
        subject=f"[Portfolio] {payload.subject}",
        recipients=[settings.mail_to],
        body=body,
        subtype=MessageType.plain,
        reply_to=[payload.email],
    )

    try:
        mailer = FastMail(conf)
        await mailer.send_message(message)
        return True
    except Exception:
        logger.exception("Failed to send contact notification email.")
        return False
