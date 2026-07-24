from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class EvaluationResult(Base):
    __tablename__ = "evaluation_results"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    project_id: Mapped[int] = mapped_column(
        ForeignKey("ad_projects.id"),
        index=True,
    )
    draft_id: Mapped[int | None] = mapped_column(
        ForeignKey("ad_drafts.id"),
        nullable=True,
        index=True,
    )
    evaluation_type: Mapped[str] = mapped_column(String(50), index=True)
    target_label: Mapped[str | None] = mapped_column(String(50), nullable=True)
    prompt_version: Mapped[str | None] = mapped_column(String(50), nullable=True)
    model_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    eval_model_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    score: Mapped[float | None] = mapped_column(Float, nullable=True)
    detail_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    success: Mapped[bool] = mapped_column(Boolean, default=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
    )

    project = relationship("AdProject", back_populates="evaluation_results")
    draft = relationship("AdDraft", back_populates="evaluation_results")
