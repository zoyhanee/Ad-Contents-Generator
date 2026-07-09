from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.ad_project import AdProject
from app.models.product import Product
from app.schemas.project import ProjectCreate


def create_project(
    db: Session,
    *,
    user_id: int,
    project: ProjectCreate,
) -> AdProject:

    # ✅ 먼저 상품이 존재하는지 + 내 상품인지 확인
    product = (
        db.query(Product)
        .filter(
            Product.id == project.product_id,
            Product.user_id == user_id,
        )
        .first()
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found.",
        )

    # ✅ 검증 통과 후 Project 생성
    db_project = AdProject(
        user_id=user_id,
        product_id=project.product_id,
    )

    db.add(db_project)
    db.commit()
    db.refresh(db_project)

    return db_project

def get_project_by_id(
    db: Session,
    *,
    project_id: int,
    user_id: int,
) -> AdProject | None:
    return (
        db.query(AdProject)
        .filter(
            AdProject.id == project_id,
            AdProject.user_id == user_id,
        )
        .first()
    )