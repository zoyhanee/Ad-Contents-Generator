from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.generate_schema import (
    GenerateRequest,
    GenerateResponse,
    RegenerateDraftRequest,
    RegenerateDraftResponse,
)
from app.services.generate_service import (
    generate_ad_drafts,
    regenerate_ad_draft,
)
from app.services.evaluation_service import (
    run_project_evaluation_background,
)
from app.dependencies import get_current_user
from app.models.user import User


router = APIRouter()


@router.post(
    "/generate",
    response_model=GenerateResponse,
    tags=["Generate"],
)
def generate(
    request: GenerateRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = generate_ad_drafts(
        db=db,
        user_id=current_user.id,
        request=request,
    )

    background_tasks.add_task(
        run_project_evaluation_background,
        result["project_id"],
    )

    return result


@router.post(
    "/generate/regenerate",
    response_model=RegenerateDraftResponse,
    tags=["Generate"],
)
def regenerate(
    request: RegenerateDraftRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return regenerate_ad_draft(
        db=db,
        user_id=current_user.id,
        request=request,
    )