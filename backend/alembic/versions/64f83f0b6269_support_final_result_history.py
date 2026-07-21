"""support final result history

Revision ID: 64f83f0b6269
Revises: bd3e5f6258bf
Create Date: 2026-07-11 20:57:47.805020

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "64f83f0b6269"
down_revision: Union[str, Sequence[str], None] = "bd3e5f6258bf"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "final_results",
        sa.Column("version", sa.Integer(), nullable=False),
    )

    with op.batch_alter_table("final_results") as batch_op:
        batch_op.drop_index("ix_final_results_project_id")
        batch_op.create_index(
            "ix_final_results_project_id",
            ["project_id"],
            unique=False,
        )

        batch_op.drop_index("ix_final_results_selected_draft_id")
        batch_op.create_index(
            "ix_final_results_selected_draft_id",
            ["selected_draft_id"],
            unique=False,
        )

        batch_op.create_unique_constraint(
            "uq_project_version",
            ["project_id", "version"],
        )


def downgrade() -> None:
    """Downgrade schema."""

    with op.batch_alter_table("final_results") as batch_op:
        batch_op.drop_constraint(
            "uq_project_version",
            type_="unique",
        )

        batch_op.drop_index("ix_final_results_selected_draft_id")
        batch_op.create_index(
            "ix_final_results_selected_draft_id",
            ["selected_draft_id"],
            unique=True,
        )

        batch_op.drop_index("ix_final_results_project_id")
        batch_op.create_index(
            "ix_final_results_project_id",
            ["project_id"],
            unique=True,
        )

    op.drop_column("final_results", "version")