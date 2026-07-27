from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, ForeignKey, Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class AdEvaluation(Base):
    __tablename__ = "ad_evaluations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

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

    slogan_quality_score: Mapped[int] = mapped_column(Integer, nullable=False)
    visual_quality_score: Mapped[int] = mapped_column(Integer, nullable=False)
    product_fidelity_score: Mapped[int] = mapped_column(Integer, nullable=False)
    strategy_alignment_score: Mapped[int] = mapped_column(Integer, nullable=False)
    slogan_visual_alignment_score: Mapped[int] = mapped_column(Integer, nullable=False)

    overall_score: Mapped[float] = mapped_column(Float, nullable=False)

    feedback: Mapped[dict] = mapped_column(JSON, nullable=False)

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
        DateTime(timezone=True),
        default=utc_now,
        nullable=False,
    )