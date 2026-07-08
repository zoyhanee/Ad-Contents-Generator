from fastapi import APIRouter, Depends
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


router = APIRouter()


@router.post(
    "/generate",
    response_model=GenerateResponse,
    tags=["Generate"],
)
def generate(
    request: GenerateRequest,
    db: Session = Depends(get_db),
):
    return generate_ad_drafts(
        db=db,
        request=request,
    )


@router.post(
    "/generate/regenerate",
    response_model=RegenerateDraftResponse,
    tags=["Generate"],
)
def regenerate(
    request: RegenerateDraftRequest,
    db: Session = Depends(get_db),
):
    return regenerate_ad_draft(
        db=db,
        request=request,
    )