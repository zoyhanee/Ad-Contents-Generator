from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.strategy_schema import StrategyInfo
from app.ml.clients.factory import create_text_model_client
from app.ml.strategy_prompt import generate_strategy_recommendation
from app.services.evaluation_service import (
    get_prompt_improvement_context,
    get_slogan_improvement_rules,
)


def recommend_strategy(
    db: Session,
    product: Product,
    strategy: StrategyInfo,
):
    text_client = create_text_model_client()

    improvement_context = get_prompt_improvement_context(
        db=db,
        min_evaluations=1,  # 연결 테스트용
    )

    slogan_improvement_rules = get_slogan_improvement_rules(
        improvement_context,
    )

    recommendation = generate_strategy_recommendation(
        client=text_client,
        product_name=product.name,
        product_description=product.description or "",
        industry=product.industry or "기타",
        price=product.price,
        mode=strategy.mode,
        platform=strategy.platform or "instagram",
        goal=strategy.goal,
        style=strategy.style,
        improvement_rules=slogan_improvement_rules,
    )

    return recommendation