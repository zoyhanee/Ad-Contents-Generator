from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import ProductCreate


def create_product(
    db: Session,
    *,
    user_id: int,
    product: ProductCreate,
) -> Product:

    db_product = Product(
        user_id=user_id,
        name=product.name,
        price=product.price,
        description=product.description,
        industry=product.industry,
        image_path=product.image_path,
    )

    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product


def get_products_by_user(
    db: Session,
    user_id: int,
) -> list[Product]:
    return (
        db.query(Product)
        .filter(Product.user_id == user_id)
        .order_by(Product.created_at.desc())
        .all()
    )


def get_product_by_id(
    db: Session,
    *,
    product_id: int,
    user_id: int,
) -> Product | None:
    return (
        db.query(Product)
        .filter(
            Product.id == product_id,
            Product.user_id == user_id,
        )
        .first()
    )