from brevo import AsyncBrevo
from brevo.transactional_emails import (
    SendTransacEmailRequestSender as Sender,
    SendTransacEmailRequestToItem as Reciever,
)
from app.utils.env import settings

client = AsyncBrevo(api_key=settings.BREVO_KEY)

async def send_email(subject: str, html: str):
    await client.transactional_emails.send_transac_email(
        subject=subject,
        html_content=html,
        sender=Sender(
            name=settings.BREVO_NAME,
            email=settings.BREVO_EMAIL,
        ),
        to=[
            Reciever(
                email=settings.ADMIN_EMAIL,
                name=settings.BREVO_NAME,
            )
        ],
    )