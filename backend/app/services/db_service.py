from sqlalchemy.orm import Session

from app.models import AdProject, AdStrategy, Product, User
from app.schemas.strategy_schema import StrategyRecommendRequest


DEV_USER_EMAIL = "dev@admaker.local"


def get_or_create_dev_user(db: Session) -> User:
    user = (
        db.query(User)
        .filter(User.email == DEV_USER_EMAIL)
        .first()
    )

    if user:
        return user

    user = User(
        email=DEV_USER_EMAIL,
        password_hash="dev-only",
        store_name="개발용 스토어",
    )

    db.add(user)
    db.flush()

    return user

def save_strategy_recommendation(
    db: Session,
    request: StrategyRecommendRequest,
    recommendation: dict,
) -> AdStrategy:
    user = get_or_create_dev_user(db)

    try:
        product = Product(
            user_id=user.id,
            name=request.product.name,
            price=int(request.product.price) if request.product.price else None,
            description=request.product.description,
            industry=request.product.category,
        )
        db.add(product)
        db.flush()

        project = AdProject(
            user_id=user.id,
            product_id=product.id,
            status="strategy_created",
        )
        db.add(project)
        db.flush()

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