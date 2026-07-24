from typing import Any

from pydantic import BaseModel, Field


class AdEvaluationRequest(BaseModel):
    # 평가 대상 식별
    project_id: int
    draft_id: int | None = None

    # 상품 정보
    product_name: str
    product_description: str | None = None

    # 원본 상품 이미지
    product_image_path: str

    # 광고 전략
    strategy: dict[str, Any]

    # 최종 사용 슬로건
    slogan: str

    # 생성된 광고 이미지
    generated_image_path: str


class EvaluationItem(BaseModel):
    score: int = Field(ge=1, le=10)
    feedback: str


class AdEvaluationResponse(BaseModel):
    slogan_quality: EvaluationItem
    visual_quality: EvaluationItem
    product_fidelity: EvaluationItem
    strategy_alignment: EvaluationItem
    slogan_visual_alignment: EvaluationItem

    overall_score: int = Field(ge=0, le=100)

    strengths: list[str]
    issues: list[str]
    improvements: list[str]