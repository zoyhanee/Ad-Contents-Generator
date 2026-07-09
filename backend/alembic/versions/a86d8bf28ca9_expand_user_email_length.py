"""expand user email length

Revision ID: a86d8bf28ca9
Revises: 38cbc7e7c235
Create Date: 2026-07-09 16:38:15.794639

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a86d8bf28ca9'
down_revision: Union[str, Sequence[str], None] = '38cbc7e7c235'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("users") as batch_op:
        batch_op.alter_column(
            "email",
            existing_type=sa.VARCHAR(length=255),
            type_=sa.String(length=320),
            existing_nullable=False,
        )


def downgrade() -> None:
    with op.batch_alter_table("users") as batch_op:
        batch_op.alter_column(
            "email",
            existing_type=sa.String(length=320),
            type_=sa.VARCHAR(length=255),
            existing_nullable=False,
        )