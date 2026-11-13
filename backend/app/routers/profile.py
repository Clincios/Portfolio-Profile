from fastapi import APIRouter, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import DbSession
from app.models import Profile
from app.schemas import ProfileOut

router = APIRouter(prefix="/api", tags=["profile"])


@router.get("/profile", response_model=ProfileOut)
def get_profile(db: DbSession) -> Profile:
    profile = db.query(Profile).order_by(Profile.id.asc()).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found. Run the seed script first.",
        )
    return profile
