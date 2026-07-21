from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.history import (
    HistoryDetailResponse,
    HistoryItemResponse,
    HistoryUpdateRequest,
    HistoryVersionResponse,
)
from app.services.history_service import (
    get_history_detail_service,
    list_history_service,
    update_history_service,
)

router = APIRouter(
    prefix="/history",
    tags=["History"],
)


@router.get(
    "",
    response_model=list[HistoryItemResponse],
)
def list_history_api(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_history_service(
        db=db,
        user_id=current_user.id,
    )
 
  
@router.get(
    "/{project_id}",
    response_model=HistoryDetailResponse,
)
def get_history_detail_api(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_history_detail_service(
        db=db,
        user_id=current_user.id,
        project_id=project_id,
    )
    

@router.patch(
    "/{project_id}",
    response_model=HistoryVersionResponse,
)
def update_history_api(
    project_id: int,
    request: HistoryUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_history_service(
        db=db,
        user_id=current_user.id,
        project_id=project_id,
        post_copy=request.post_copy,
        image_feedback=request.image_feedback,
    )