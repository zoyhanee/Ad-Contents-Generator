from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.crud.project import create_project
from app.db.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.project import (
    ProjectCreate,
    ProjectResponse,
)

router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
)


@router.post(
    "",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_project_api(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_project(
        db=db,
        user_id=current_user.id,
        project=project,
    )