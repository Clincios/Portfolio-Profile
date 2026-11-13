from typing import List

from fastapi import APIRouter

from app.dependencies import DbSession
from app.models import Education
from app.schemas import EducationOut

router = APIRouter(prefix="/api", tags=["education"])


@router.get("/education", response_model=List[EducationOut])
def get_education(db: DbSession) -> List[Education]:
    return (
        db.query(Education)
        .order_by(Education.sort_order.asc(), Education.id.asc())
        .all()
    )
