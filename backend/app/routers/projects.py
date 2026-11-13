from typing import List, Optional

from fastapi import APIRouter, Query

from app.dependencies import DbSession
from app.models import Project
from app.schemas import ProjectOut

router = APIRouter(prefix="/api", tags=["projects"])


@router.get("/projects", response_model=List[ProjectOut])
def get_projects(
    db: DbSession,
    category: Optional[str] = Query(default=None),
) -> List[Project]:
    query = db.query(Project)
    if category and category != "all":
        query = query.filter(Project.category == category)
    return query.order_by(Project.sort_order.asc(), Project.id.asc()).all()
