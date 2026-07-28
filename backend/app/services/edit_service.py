from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.ad_draft import AdDraft
from app.models.ad_project import AdProject

from app.schemas.edit import (
    EditRequest,
    EditResponse,
)

from app.services.edit_planner import EditPlanner


def edit_ad(
    db: Session,
    user_id: int,
    request: EditRequest,
) -> EditResponse:

    # 1. Draft 조회
    draft = (
        db.query(AdDraft)
        .filter(AdDraft.id == request.draft_id)
        .first()
    )

    if draft is None:
        raise HTTPException(
            status_code=404,
            detail="광고 초안을 찾을 수 없습니다.",
        )

    # 2. Project 조회
    project = (
        db.query(AdProject)
        .filter(AdProject.id == draft.project_id)
        .first()
    )

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="프로젝트를 찾을 수 없습니다.",
        )

    # 3. 권한 확인
    if project.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="수정 권한이 없습니다.",
        )

    # 4. Edit Plan 생성
    planner = EditPlanner()

    plan = planner.create_plan(
        request.instruction,
    )

    # 5. (현재는 Planner 결과만 반환)
    return EditResponse(
        success=True,
        message=plan.prompt,
    )