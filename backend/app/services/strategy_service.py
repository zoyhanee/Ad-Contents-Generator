from app.models.product import Product
from app.schemas.strategy_schema import StrategyInfo
from app.ml.clients.factory import create_text_model_client
from app.ml.strategy_prompt import generate_strategy_recommendation
from app.services.evaluation_service import evaluate_and_log_slogans
from app.core.config import settings


def recommend_strategy(
    product: Product,
    strategy: StrategyInfo,
    db=None,
    project_id: int | None = None,
):
    text_client = create_text_model_client()

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
    )

    slogans = recommendation.get("slogans", [])

    if slogans:
        evaluate_and_log_slogans(
            slogans=slogans,
            product_name=product.name,
            product_description=product.description or "",
            platform=strategy.platform or "instagram",
            goal=strategy.goal,
            style=strategy.style,
            db=db,
            project_id=project_id,
            model_name=settings.TEXT_MODEL_NAME,
        )

    return recommendation
