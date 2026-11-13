from typing import List

from fastapi import APIRouter

from app.dependencies import DbSession
from app.models import Experience
from app.schemas import ExperienceOut

router = APIRouter(prefix="/api", tags=["experience"])


@router.get("/experience", response_model=List[ExperienceOut])
def get_experience(db: DbSession) -> List[Experience]:
    return (
        db.query(Experience)
        .order_by(Experience.sort_order.asc(), Experience.id.asc())
        .all()
    )
