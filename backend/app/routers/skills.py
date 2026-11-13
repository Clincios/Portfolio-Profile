from typing import List

from fastapi import APIRouter
from sqlalchemy.orm import joinedload

from app.dependencies import DbSession
from app.models import SkillCategory
from app.schemas import SkillCategoryOut

router = APIRouter(prefix="/api", tags=["skills"])


@router.get("/skills", response_model=List[SkillCategoryOut])
def get_skills(db: DbSession) -> List[SkillCategory]:
    return (
        db.query(SkillCategory)
        .options(joinedload(SkillCategory.skills))
        .order_by(SkillCategory.sort_order.asc(), SkillCategory.id.asc())
        .all()
    )
