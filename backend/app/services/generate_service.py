from fastapi import HTTPException
from sqlalchemy.orm import Session
from pathlib import Path
from uuid import uuid4

from app.models import AdDraft, AdProject
from app.schemas.generate_schema import GenerateRequest, RegenerateDraftRequest
from app.ml.generation_pipeline import generate_drafts
from app.ml.image_clients.factory import create_image_model_client
from app.crud.project import get_project_by_id


def generate_ad_drafts(
    db: Session,
    user_id: int,
    request: GenerateRequest,
) -> dict:
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

    if project.strategy is None:
        raise HTTPException(
            status_code=404,
            detail="Strategy not found.",
        )
    
    existing_drafts = (
        db.query(AdDraft)
        .filter(AdDraft.project_id == project.id)
        .all()
    )

    if existing_drafts:
        return {
            "project_id": project.id,
            "drafts": [
                {
                    "id": draft.draft_label,
                    "title": draft.title,
                    "version": draft.version,
                    "image_path": draft.image_path,
                    "image_prompt": draft.image_prompt,
                }
                for draft in existing_drafts
            ],
        }

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
    

def regenerate_ad_draft(
    db: Session,
    user_id: int,
    request: RegenerateDraftRequest,
) -> dict:
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

    draft = (
        db.query(AdDraft)
        .filter(
            AdDraft.project_id == request.project_id,
            AdDraft.draft_label == request.draft_id,
        )
        .first()
    )

    if draft is None:
        raise HTTPException(
            status_code=404,
            detail="Draft not found.",
        )

    try:
        image_client = create_image_model_client()

        regenerate_prompt = f"""
Edit the provided advertising image according to the user's feedback.

Preserve the original product identity and important visual details.
Keep the overall image suitable for professional advertising.

User feedback:
{request.feedback}
"""

        image_bytes = image_client.generate(
            prompt=regenerate_prompt,
            source_image_path=draft.image_path,
        )

        image_path = (
            Path("storage/generated")
            / f"{uuid4().hex}.png"
        )

        image_path.write_bytes(image_bytes)

        draft.image_path = str(image_path)
        draft.image_prompt = regenerate_prompt
        draft.version += 1

        db.commit()
        db.refresh(draft)

        return {
            "project_id": project.id,
            "draft": {
                "id": draft.draft_label,
                "title": draft.title,
                "version": draft.version,
                "image_path": draft.image_path,
                "image_prompt": draft.image_prompt,
            },
        }

    except Exception:
        db.rollback()
        raise