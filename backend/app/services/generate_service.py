from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import AdDraft, AdProject
from app.schemas.generate_schema import GenerateRequest


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

        draft_data = [
            {
                "id": "A",
                "title": "시안 A",
                "version": 1,
                "image_path": None,
            },
            {
                "id": "B",
                "title": "시안 B",
                "version": 1,
                "image_path": None,
            },
            {
                "id": "C",
                "title": "시안 C",
                "version": 1,
                "image_path": None,
            },
        ]

        for draft in draft_data:
            db.add(
                AdDraft(
                    project_id=project.id,
                    draft_label=draft["id"],
                    title=draft["title"],
                    version=draft["version"],
                    image_path=draft["image_path"],
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