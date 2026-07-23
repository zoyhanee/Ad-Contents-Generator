"""repair final result version schema

Revision ID: 3f9bc0a15350
Revises: ef55ffd4cc38
Create Date: 2026-07-21 10:03:08.754021

"""
from typing import Sequence, Union


revision: str = "3f9bc0a15350"
down_revision: Union[str, Sequence[str], None] = "ef55ffd4cc38"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """No-op.

    The final_results.version column and uq_project_version constraint
    were already added by revision 64f83f0b6269.
    """
    pass


def downgrade() -> None:
    """No-op."""
    pass