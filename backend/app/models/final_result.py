from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class FinalResult(Base):
    __tablename__ = "final_results"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    project_id: Mapped[int] = mapped_column(
        ForeignKey("ad_projects.id"),
        unique=True,
        index=True,
    )
    selected_draft_id: Mapped[int] = mapped_column(
        ForeignKey("ad_drafts.id"),
        unique=True,
        index=True,
    )
    image_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    saved_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
    )

    project = relationship("AdProject", back_populates="final_result")
    selected_draft = relationship("AdDraft", back_populates="final_result")
