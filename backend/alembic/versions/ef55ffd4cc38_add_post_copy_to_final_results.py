"""add post_copy to final_results

Revision ID: ef55ffd4cc38
Revises: 64f83f0b6269
Create Date: 2026-07-21 09:11:34.756014

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ef55ffd4cc38'
down_revision: Union[str, Sequence[str], None] = '64f83f0b6269'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "final_results",
        sa.Column(
            "post_copy",
            sa.Text(),
            nullable=True,
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column(
        "final_results",
        "post_copy",
    )
