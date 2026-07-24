from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.strategy_schema import StrategyRecommendRequest
from app.services.db_service import save_strategy_recommendation
from app.services.strategy_service import recommend_strategy
from app.dependencies import get_current_user
from app.models.user import User
from app.crud.project import get_project_by_id


router = APIRouter(prefix="/strategy", tags=["Strategy"])


@router.post("/recommend")
def recommend(
    request: StrategyRecommendRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    project = get_project_by_id(
        db=db,
        project_id=request.project_id,
        user_id=current_user.id,
    )

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found.",
        )

    recommendation = recommend_strategy(
        product=project.product,
        strategy=request.strategy,
        db=db,
        project_id=project.id,
    )

    saved_strategy = save_strategy_recommendation(
        db=db,
        user_id=current_user.id,
        request=request,
        recommendation=recommendation,
    )

    return {
        **recommendation,
        "project_id": saved_strategy.project_id,
    }
