from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies import get_current_user
from app.models.user import User

from app.schemas.edit import (
    EditRequest,
    EditResponse,
)

from app.services.edit_service import edit_ad

router = APIRouter()


@router.post(
    "/edit",
    response_model=EditResponse,
    tags=["Edit"],
)
def edit(
    request: EditRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return edit_ad(
        db=db,
        user_id=current_user.id,
        request=request,
    )