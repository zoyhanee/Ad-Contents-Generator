"""add oauth fields to users

Revision ID: c1f4a8d7e2b9
Revises: bd3e5f6258bf
Create Date: 2026-07-16 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c1f4a8d7e2b9"
down_revision: Union[str, Sequence[str], None] = "bd3e5f6258bf"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("users") as batch_op:
        batch_op.alter_column(
            "password_hash",
            existing_type=sa.String(length=255),
            nullable=True,
        )
        batch_op.add_column(
            sa.Column(
                "provider",
                sa.String(length=20),
                nullable=False,
                server_default="local",
            )
        )
        batch_op.add_column(
            sa.Column(
                "provider_user_id",
                sa.String(length=255),
                nullable=True,
            )
        )
        batch_op.create_index(
            "ix_users_provider_user_id",
            ["provider_user_id"],
        )

    with op.batch_alter_table("users") as batch_op:
        batch_op.alter_column(
            "provider",
            server_default=None,
        )


def downgrade() -> None:
    with op.batch_alter_table("users") as batch_op:
        batch_op.drop_index("ix_users_provider_user_id")
        batch_op.drop_column("provider_user_id")
        batch_op.drop_column("provider")
        batch_op.alter_column(
            "password_hash",
            existing_type=sa.String(length=255),
            nullable=False,
        )
