from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import AdDraft, AdProject
from app.schemas.generate_schema import GenerateRequest
from app.ml.generation_pipeline import generate_drafts


def generate_ad_drafts(
    db: Session,
    request: GenerateRequest,
) -> dict:
    project = (
        db.query(AdProject)
        .filter(AdProject.id == request.project_id)
        .first()
    )

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found.",
        )

    if project.strategy is None:
        raise HTTPException(
            status_code=404,
            detail="Strategy not found.",
        )

    try:
        project.strategy.selected_slogan = request.selected_slogan

        platform = (
            project.strategy.selected_platforms[0]
            if project.strategy.selected_platforms
            else "instagram"
        )

        draft_data = generate_drafts(
            product_name=project.product.name,
            product_description=project.product.description,
            product_image_path=project.product.image_path,
            platform=platform,
            style=project.strategy.selected_style,
            selected_slogan=request.selected_slogan,
        )

        for draft in draft_data:
            db.add(
                AdDraft(
                    project_id=project.id,
                    draft_label=draft["id"],
                    title=draft["title"],
                    version=draft["version"],
                    image_path=draft["image_path"],
                    image_prompt=draft["image_prompt"],
                )
            )

        project.status = "generated"

        db.commit()

        return {
            "project_id": project.id,
            "drafts": draft_data,
        }

    except Exception:
        db.rollback()
        raise