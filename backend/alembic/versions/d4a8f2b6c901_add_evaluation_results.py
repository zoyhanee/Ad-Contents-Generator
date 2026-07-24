"""add evaluation results

Revision ID: d4a8f2b6c901
Revises: ac7d1c5d4ae6
Create Date: 2026-07-23 16:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d4a8f2b6c901"
down_revision: Union[str, Sequence[str], None] = "ac7d1c5d4ae6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "evaluation_results",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("draft_id", sa.Integer(), nullable=True),
        sa.Column("evaluation_type", sa.String(length=50), nullable=False),
        sa.Column("target_label", sa.String(length=50), nullable=True),
        sa.Column("prompt_version", sa.String(length=50), nullable=True),
        sa.Column("model_name", sa.String(length=100), nullable=True),
        sa.Column("eval_model_name", sa.String(length=100), nullable=True),
        sa.Column("score", sa.Float(), nullable=True),
        sa.Column("detail_json", sa.JSON(), nullable=True),
        sa.Column("success", sa.Boolean(), nullable=False),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["draft_id"], ["ad_drafts.id"]),
        sa.ForeignKeyConstraint(["project_id"], ["ad_projects.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_evaluation_results_id"),
        "evaluation_results",
        ["id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_evaluation_results_project_id"),
        "evaluation_results",
        ["project_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_evaluation_results_draft_id"),
        "evaluation_results",
        ["draft_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_evaluation_results_evaluation_type"),
        "evaluation_results",
        ["evaluation_type"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(
        op.f("ix_evaluation_results_evaluation_type"),
        table_name="evaluation_results",
    )
    op.drop_index(
        op.f("ix_evaluation_results_draft_id"),
        table_name="evaluation_results",
    )
    op.drop_index(
        op.f("ix_evaluation_results_project_id"),
        table_name="evaluation_results",
    )
    op.drop_index(
        op.f("ix_evaluation_results_id"),
        table_name="evaluation_results",
    )
    op.drop_table("evaluation_results")
