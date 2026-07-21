"""merge history and oauth migration heads

Revision ID: ac7d1c5d4ae6
Revises: 3f9bc0a15350, c1f4a8d7e2b9
Create Date: 2026-07-21 18:51:42.008654

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ac7d1c5d4ae6'
down_revision: Union[str, Sequence[str], None] = ('3f9bc0a15350', 'c1f4a8d7e2b9')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
