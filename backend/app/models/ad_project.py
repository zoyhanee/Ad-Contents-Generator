from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class AdProject(Base):
    __tablename__ = "ad_projects"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        index=True,
    )
    status: Mapped[str] = mapped_column(String(50), default="draft")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
    )

    user = relationship("User", back_populates="ad_projects")
    product = relationship("Product", back_populates="ad_projects")
    strategy = relationship(
        "AdStrategy",
        back_populates="project",
        uselist=False,
    )
    drafts = relationship("AdDraft", back_populates="project")
    final_results = relationship(
        "FinalResult",
        back_populates="project",
        cascade="all, delete-orphan",
    )
    evaluation_results = relationship(
        "EvaluationResult",
        back_populates="project",
        cascade="all, delete-orphan",
    )
