"""repair final result version schema

Revision ID: 3f9bc0a15350
Revises: ef55ffd4cc38
Create Date: 2026-07-21 10:03:08.754021

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3f9bc0a15350'
down_revision: Union[str, Sequence[str], None] = 'ef55ffd4cc38'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "final_results",
        sa.Column(
            "version",
            sa.Integer(),
            nullable=False,
            server_default="1",
        ),
    )

    with op.batch_alter_table("final_results") as batch_op:
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

    op.drop_column(
        "final_results",
        "version",
    )