from fastapi import APIRouter

from app.dependencies import DbSession
from app.models import ContactMessage
from app.schemas import ContactCreate, ContactResponse
from app.services.email import send_contact_notification

router = APIRouter(prefix="/api", tags=["contact"])


@router.post("/contact", response_model=ContactResponse)
async def submit_contact(payload: ContactCreate, db: DbSession) -> ContactResponse:
    message = ContactMessage(
        name=payload.name.strip(),
        email=str(payload.email).strip(),
        subject=payload.subject.strip(),
        message=payload.message.strip(),
    )
    db.add(message)
    db.commit()
    db.refresh(message)

    await send_contact_notification(payload)

    return ContactResponse(
        success=True,
        message="Thanks for reaching out! I will get back to you soon.",
    )
