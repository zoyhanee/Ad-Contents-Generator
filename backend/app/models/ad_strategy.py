from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, ForeignKey, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class AdStrategy(Base):
    __tablename__ = "ad_strategies"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    project_id: Mapped[int] = mapped_column(
        ForeignKey("ad_projects.id"),
        unique=True,
        index=True,
    )
    strategy_mode: Mapped[str] = mapped_column(String(50))
    reuse_tone: Mapped[bool] = mapped_column(Boolean, default=False)
    selected_platforms: Mapped[list[str]] = mapped_column(JSON, default=list)
    poster_size: Mapped[str | None] = mapped_column(String(50), nullable=True)
    selected_goal: Mapped[str | None] = mapped_column(String(50), nullable=True)
    selected_style: Mapped[str | None] = mapped_column(String(50), nullable=True)
    strategy_title: Mapped[str | None] = mapped_column(String(200), nullable=True)
    strategy_description: Mapped[str | None] = mapped_column(Text, nullable=True)
    slogans: Mapped[list[str]] = mapped_column(JSON, default=list)
    selected_slogan: Mapped[str | None] = mapped_column(String(300), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
    )

    project = relationship("AdProject", back_populates="strategy")
