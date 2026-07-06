from fastapi import APIRouter

from app.schemas.strategy_schema import StrategyRecommendRequest
from app.services.strategy_service import recommend_strategy

router = APIRouter(prefix="/strategy", tags=["Strategy"])


@router.post("/recommend")
def recommend(request: StrategyRecommendRequest):
    return recommend_strategy(request)