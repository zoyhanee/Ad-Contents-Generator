from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.services.project_service import (
    create_project_service,
    finalize_project_service,
    list_projects_service,
)
from app.db.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.project import (
    FinalizeProjectRequest,
    FinalResultResponse,
    ProjectCreate,
    ProjectResponse,
    ProjectSummaryResponse,
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
    return create_project_service(
        db=db,
        user_id=current_user.id,
        project=project,
    )


@router.get(
    "",
    response_model=list[ProjectSummaryResponse],
)
def list_projects_api(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_projects_service(
        db=db,
        user_id=current_user.id,
    )
    

@router.post(
    "/{project_id}/finalize",
    response_model=FinalResultResponse,
    status_code=status.HTTP_201_CREATED,
)
def finalize_project_api(
    project_id: int,
    request: FinalizeProjectRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return finalize_project_service(
        db=db,
        user_id=current_user.id,
        project_id=project_id,
        request=request,
    )