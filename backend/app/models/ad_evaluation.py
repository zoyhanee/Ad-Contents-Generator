from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, JSON, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class AdEvaluation(Base):
    __tablename__ = "ad_evaluations"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    project_id: Mapped[int] = mapped_column(
        ForeignKey("ad_projects.id"),
        nullable=False,
        index=True,
    )

    draft_id: Mapped[int | None] = mapped_column(
        ForeignKey("ad_drafts.id"),
        nullable=True,
        index=True,
    )

    # 개별 평가 점수
    slogan_quality_score: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    visual_quality_score: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    product_fidelity_score: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    strategy_alignment_score: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    slogan_visual_alignment_score: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    overall_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    # 평가 상세 내용
    feedback: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
    )

    strengths: Mapped[list] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    issues: Mapped[list] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    improvements: Mapped[list] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime,
        nullable=False,
    )