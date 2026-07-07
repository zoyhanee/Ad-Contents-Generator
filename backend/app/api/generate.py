from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.generate_schema import GenerateRequest, GenerateResponse
from app.services.generate_service import generate_ad_drafts


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