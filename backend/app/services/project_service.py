from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.crud.project import (
    create_project,
    get_project_by_id,
    get_projects_by_user,
)
from app.models import AdDraft, FinalResult
from app.schemas.project import (
    FinalizeProjectRequest,
    ProjectCreate,
)


def create_project_service(
    db: Session,
    *,
    user_id: int,
    project: ProjectCreate,
):
    return create_project(
        db=db,
        user_id=user_id,
        project=project,
    )


def list_projects_service(
    db: Session,
    *,
    user_id: int,
):
    return get_projects_by_user(
        db=db,
        user_id=user_id,
    )
    
    
def finalize_project_service(
    db: Session,
    *,
    user_id: int,
    project_id: int,
    request: FinalizeProjectRequest,
):
    project = get_project_by_id(
        db=db,
        project_id=project_id,
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
            AdDraft.project_id == project.id,
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
        (
            db.query(AdDraft)
            .filter(AdDraft.project_id == project.id)
            .update(
                {AdDraft.is_selected: False},
                synchronize_session=False,
            )
        )

        draft.is_selected = True

        latest_version = (
            db.query(func.max(FinalResult.version))
            .filter(FinalResult.project_id == project.id)
            .scalar()
        )

        next_version = (latest_version or 0) + 1

        final_result = FinalResult(
            project_id=project.id,
            version=next_version,
            selected_draft_id=draft.id,
            image_path=draft.image_path,
            post_copy=request.post_copy or draft.post_copy,
        )

        db.add(final_result)

        project.status = "completed"

        db.commit()
        db.refresh(final_result)

        return final_result

    except Exception:
        db.rollback()
        raise