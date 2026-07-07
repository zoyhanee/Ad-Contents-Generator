from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class AdDraft(Base):
    __tablename__ = "ad_drafts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    project_id: Mapped[int] = mapped_column(
        ForeignKey("ad_projects.id"),
        index=True,
    )
    draft_label: Mapped[str] = mapped_column(String(10))
    title: Mapped[str | None] = mapped_column(String(100), nullable=True)
    version: Mapped[int] = mapped_column(Integer, default=1)
    image_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    image_prompt: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    feedback: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_selected: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
    )

    project = relationship("AdProject", back_populates="drafts")
    final_result = relationship(
        "FinalResult",
        back_populates="selected_draft",
        uselist=False,
    )
