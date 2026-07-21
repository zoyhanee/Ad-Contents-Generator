from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException
from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from app.ml.image_clients.factory import create_image_model_client
from app.models import AdProject, FinalResult, Product


def list_history_service(
    db: Session,
    *,
    user_id: int,
) -> list[dict]:
    latest_versions = (
        db.query(
            FinalResult.project_id.label("project_id"),
            func.max(FinalResult.version).label("latest_version"),
        )
        .join(
            AdProject,
            AdProject.id == FinalResult.project_id,
        )
        .filter(
            AdProject.user_id == user_id,
        )
        .group_by(
            FinalResult.project_id,
        )
        .subquery()
    )

    rows = (
        db.query(
            FinalResult,
            Product.name.label("product_name"),
        )
        .join(
            latest_versions,
            and_(
                FinalResult.project_id
                == latest_versions.c.project_id,
                FinalResult.version
                == latest_versions.c.latest_version,
            ),
        )
        .join(
            AdProject,
            AdProject.id == FinalResult.project_id,
        )
        .join(
            Product,
            Product.id == AdProject.product_id,
        )
        .filter(
            AdProject.user_id == user_id,
        )
        .order_by(
            FinalResult.saved_at.desc(),
        )
        .all()
    )

    return [
        {
            "project_id": final_result.project_id,
            "product_name": product_name,
            "version": final_result.version,
            "image_path": final_result.image_path,
            "post_copy": final_result.post_copy,
            "saved_at": final_result.saved_at,
        }
        for final_result, product_name in rows
    ]
   
    
def get_history_detail_service(
    db: Session,
    *,
    user_id: int,
    project_id: int,
) -> dict:
    project = (
        db.query(AdProject)
        .filter(
            AdProject.id == project_id,
            AdProject.user_id == user_id,
        )
        .first()
    )

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="History not found.",
        )

    final_results = (
        db.query(FinalResult)
        .filter(
            FinalResult.project_id == project_id,
        )
        .order_by(
            FinalResult.version.desc(),
        )
        .all()
    )

    if not final_results:
        raise HTTPException(
            status_code=404,
            detail="Final result not found.",
        )

    latest_result = final_results[0]
    product = project.product

    return {
        "project_id": project.id,

        "product_id": product.id,
        "product_name": product.name,
        "product_price": product.price,
        "product_description": product.description,
        "product_industry": product.industry,

        "latest_version": latest_result.version,
        "image_path": latest_result.image_path,
        "post_copy": latest_result.post_copy,
        "saved_at": latest_result.saved_at,

        "versions": [
            {
                "id": result.id,
                "version": result.version,
                "selected_draft_id": (
                    result.selected_draft_id
                ),
                "image_path": result.image_path,
                "post_copy": result.post_copy,
                "saved_at": result.saved_at,
            }
            for result in final_results
        ],
    }
    

def update_history_service(
    db: Session,
    *,
    user_id: int,
    project_id: int,
    post_copy: str | None,
    image_feedback: str | None,
) -> FinalResult:
    project = (
        db.query(AdProject)
        .filter(
            AdProject.id == project_id,
            AdProject.user_id == user_id,
        )
        .first()
    )

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="History not found.",
        )

    latest_result = (
        db.query(FinalResult)
        .filter(
            FinalResult.project_id == project_id,
        )
        .order_by(
            FinalResult.version.desc(),
        )
        .first()
    )

    if latest_result is None:
        raise HTTPException(
            status_code=404,
            detail="Final result not found.",
        )

    next_version = latest_result.version + 1

    try:
        new_image_path = latest_result.image_path

        normalized_feedback = (
            image_feedback.strip()
            if image_feedback
            else ""
        )

        if normalized_feedback:
            if not latest_result.image_path:
                raise HTTPException(
                    status_code=400,
                    detail="No image available to edit.",
                )

            source_image_path = Path(
                latest_result.image_path
            )

            if not source_image_path.exists():
                raise HTTPException(
                    status_code=404,
                    detail="Source image not found.",
                )

            image_client = create_image_model_client()

            edit_prompt = f"""
    Edit the provided advertising image according to the user's feedback.

    Preserve the original product identity, shape, branding,
    and important visual details unless the user explicitly
    requests otherwise.

    Keep the result suitable for professional advertising.

    User feedback:
    {normalized_feedback}
    """

            image_bytes = image_client.generate(
                prompt=edit_prompt,
                source_image_path=str(
                    source_image_path
                ),
            )

            output_dir = Path(
                "storage/generated"
            )
            output_dir.mkdir(
                parents=True,
                exist_ok=True,
            )

            generated_path = (
                output_dir
                / f"{uuid4().hex}.png"
            )

            generated_path.write_bytes(
                image_bytes
            )

            new_image_path = str(
                generated_path
            )

        new_result = FinalResult(
            project_id=project.id,
            version=next_version,
            selected_draft_id=(
                latest_result.selected_draft_id
            ),
            image_path=new_image_path,
            post_copy=post_copy,
        )

        db.add(new_result)
        db.commit()
        db.refresh(new_result)

        return new_result

    except HTTPException:
        db.rollback()
        raise

    except Exception:
        db.rollback()
        raise