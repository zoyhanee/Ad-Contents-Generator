from fastapi import HTTPException
from sqlalchemy.orm import Session
from pathlib import Path
from uuid import uuid4

from app.models import AdDraft, AdProject
from app.schemas.generate_schema import GenerateRequest, RegenerateDraftRequest
from app.ml.generation_pipeline import generate_drafts
from app.ml.image_clients.factory import create_image_model_client
from app.crud.project import get_project_by_id
from app.ml.clients.factory import create_text_model_client
from app.ml.post_copy_generator import generate_post_copy


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

    try:
        # 요청으로 들어온 새 슬로건
        requested_slogan = request.selected_slogan.strip()

        # 기존 시안을 생성할 때 사용했던 슬로건
        previous_slogan = (
            project.strategy.selected_slogan or ""
        ).strip()

        existing_drafts = (
            db.query(AdDraft)
            .filter(AdDraft.project_id == project.id)
            .all()
        )

        print(
            "[GENERATE SERVICE]",
            {
                "project_id": project.id,
                "previous_slogan": previous_slogan,
                "requested_slogan": requested_slogan,
                "existing_draft_count": len(existing_drafts),
            },
        )

        # 기존 시안이 있고 슬로건도 동일하면 기존 결과 재사용
        if (
            existing_drafts
            and previous_slogan == requested_slogan
        ):
            print(
                "[GENERATE SERVICE] "
                "같은 슬로건이므로 기존 시안을 반환합니다."
            )

            return {
                "project_id": project.id,
                "drafts": [
                    {
                        "id": draft.draft_label,
                        "title": draft.title,
                        "version": draft.version,
                        "image_path": draft.image_path,
                        "image_prompt": draft.image_prompt,
                        "post_copy": draft.post_copy,
                    }
                    for draft in existing_drafts
                ],
            }

        # 기존 시안이 있지만 슬로건이 변경됐다면 기존 시안 제거
        if existing_drafts:
            print(
                "[GENERATE SERVICE] "
                "슬로건이 변경되어 기존 시안을 삭제합니다."
            )

            for draft in existing_drafts:
                # 기존 이미지 파일 삭제
                if draft.image_path:
                    image_path = Path(draft.image_path)

                    if image_path.exists():
                        try:
                            image_path.unlink()
                        except OSError as e:
                            print(
                                "[GENERATE SERVICE] "
                                f"기존 이미지 삭제 실패: {e}"
                            )

                db.delete(draft)

            # DELETE 쿼리를 먼저 DB에 반영
            db.flush()

        # 변경된 슬로건을 전략에 반영
        project.strategy.selected_slogan = requested_slogan

        platform = (
            project.strategy.selected_platforms[0]
            if project.strategy.selected_platforms
            else "instagram"
        )

        print(
            "[GENERATE SERVICE] 새 시안 생성 시작",
            {
                "selected_slogan": requested_slogan,
                "platform": platform,
                "image_width": request.image_width,
                "image_height": request.image_height,
            },
        )

        draft_data = generate_drafts(
            product_name=project.product.name,
            product_description=project.product.description,
            product_image_path=project.product.image_path,
            platform=platform,
            style=project.strategy.selected_style,
            selected_slogan=requested_slogan,
            image_width=request.image_width,
            image_height=request.image_height,
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
                    post_copy=draft["post_copy"],
                )
            )

        project.status = "generated"

        db.commit()

        print(
            "[GENERATE SERVICE] 새 시안 생성 완료",
            {
                "project_id": project.id,
                "selected_slogan": requested_slogan,
                "draft_count": len(draft_data),
            },
        )

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
        text_client = create_text_model_client()

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
        platform = (
            project.strategy.selected_platforms[0]
            if project.strategy.selected_platforms
            else "instagram"
        )

        concepts = {
            "A": (
                "제품 중심형: 제품의 형태, 소재, "
                "기능적 특징을 강하게 강조"
            ),
            "B": (
                "라이프스타일형: 고객이 제품을 실제로 사용하는 "
                "자연스러운 일상 장면을 강조"
            ),
            "C": (
                "캠페인형: 광고 슬로건과 브랜드 메시지가 "
                "강하게 느껴지는 상징적인 비주얼을 강조"
            ),
        }

        concept = concepts.get(
            draft.draft_label,
            "상품의 매력을 효과적으로 전달하는 광고",
        )

        post_copy = generate_post_copy(
            client=text_client,
            product_name=project.product.name,
            product_description=project.product.description,
            platform=platform,
            selected_slogan=(
                project.strategy.selected_slogan or ""
            ),
            concept=concept,
            feedback=request.feedback,
        )
        
        draft.image_path = str(image_path)
        draft.image_prompt = regenerate_prompt
        draft.post_copy = post_copy
        draft.feedback = request.feedback
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
                "post_copy": draft.post_copy,
            },
        }

    except Exception:
        db.rollback()
        raise