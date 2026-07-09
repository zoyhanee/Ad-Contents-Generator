from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models import AdProject, AdStrategy
from app.schemas.strategy_schema import StrategyRecommendRequest
from app.crud.project import get_project_by_id


def save_strategy_recommendation(
    db: Session,
    *,
    user_id: int,
    request: StrategyRecommendRequest,
    recommendation: dict,
) -> AdStrategy:
    project = get_project_by_id(
        db=db,
        project_id=request.project_id,
        user_id=user_id,
    )

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found.",
        )

    try:
        strategy = AdStrategy(
            project_id=project.id,
            strategy_mode=request.strategy.mode,
            reuse_tone=request.strategy.reuse_tone,
            selected_platforms=[request.strategy.platform],
            poster_size=request.strategy.poster_size,
            selected_goal=request.strategy.goal,
            selected_style=request.strategy.style,
            strategy_title=recommendation["strategy_title"],
            strategy_description=recommendation["strategy_description"],
            slogans=recommendation["slogans"],
        )
        
        db.add(strategy)
        db.commit()
        db.refresh(strategy)

        return strategy

    except Exception:
        db.rollback()
        raise