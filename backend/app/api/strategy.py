from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.strategy_schema import StrategyRecommendRequest
from app.services.db_service import save_strategy_recommendation
from app.services.strategy_service import recommend_strategy


router = APIRouter(prefix="/strategy", tags=["Strategy"])


@router.post("/recommend")
def recommend(
    request: StrategyRecommendRequest,
    db: Session = Depends(get_db),
):
    recommendation = recommend_strategy(request)

    save_strategy_recommendation(
        db=db,
        request=request,
        recommendation=recommendation,
    )

    return recommendation