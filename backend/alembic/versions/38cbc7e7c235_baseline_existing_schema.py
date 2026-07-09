"""baseline existing schema

Revision ID: 38cbc7e7c235
Revises: 
Create Date: 2026-07-09 16:34:07.670095

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '38cbc7e7c235'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column(
            "password_hash",
            sa.String(length=255),
            nullable=False,
        ),
        sa.Column(
            "store_name",
            sa.String(length=100),
            nullable=True,
        ),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_users_id",
        "users",
        ["id"],
        unique=False,
    )
    op.create_index(
        "ix_users_email",
        "users",
        ["email"],
        unique=True,
    )

    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column(
            "name",
            sa.String(length=100),
            nullable=False,
        ),
        sa.Column("price", sa.Integer(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "industry",
            sa.String(length=50),
            nullable=True,
        ),
        sa.Column(
            "image_path",
            sa.String(length=500),
            nullable=True,
        ),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_products_id",
        "products",
        ["id"],
        unique=False,
    )
    op.create_index(
        "ix_products_user_id",
        "products",
        ["user_id"],
        unique=False,
    )

    op.create_table(
        "ad_projects",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column(
            "status",
            sa.String(length=50),
            nullable=False,
        ),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["product_id"],
            ["products.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_ad_projects_id",
        "ad_projects",
        ["id"],
        unique=False,
    )
    op.create_index(
        "ix_ad_projects_product_id",
        "ad_projects",
        ["product_id"],
        unique=False,
    )
    op.create_index(
        "ix_ad_projects_user_id",
        "ad_projects",
        ["user_id"],
        unique=False,
    )

    op.create_table(
        "ad_drafts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column(
            "draft_label",
            sa.String(length=10),
            nullable=False,
        ),
        sa.Column(
            "title",
            sa.String(length=100),
            nullable=True,
        ),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column(
            "image_path",
            sa.String(length=500),
            nullable=True,
        ),
        sa.Column("image_prompt", sa.Text(), nullable=True),
        sa.Column("post_copy", sa.Text(), nullable=True),
        sa.Column("feedback", sa.Text(), nullable=True),
        sa.Column("is_selected", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["ad_projects.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_ad_drafts_id",
        "ad_drafts",
        ["id"],
        unique=False,
    )
    op.create_index(
        "ix_ad_drafts_project_id",
        "ad_drafts",
        ["project_id"],
        unique=False,
    )

    op.create_table(
        "ad_strategies",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column(
            "strategy_mode",
            sa.String(length=50),
            nullable=False,
        ),
        sa.Column("reuse_tone", sa.Boolean(), nullable=False),
        sa.Column("selected_platforms", sa.JSON(), nullable=False),
        sa.Column(
            "poster_size",
            sa.String(length=50),
            nullable=True,
        ),
        sa.Column(
            "selected_goal",
            sa.String(length=50),
            nullable=True,
        ),
        sa.Column(
            "selected_style",
            sa.String(length=50),
            nullable=True,
        ),
        sa.Column(
            "strategy_title",
            sa.String(length=200),
            nullable=True,
        ),
        sa.Column(
            "strategy_description",
            sa.Text(),
            nullable=True,
        ),
        sa.Column("slogans", sa.JSON(), nullable=False),
        sa.Column(
            "selected_slogan",
            sa.String(length=300),
            nullable=True,
        ),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["ad_projects.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_ad_strategies_id",
        "ad_strategies",
        ["id"],
        unique=False,
    )
    op.create_index(
        "ix_ad_strategies_project_id",
        "ad_strategies",
        ["project_id"],
        unique=True,
    )

    op.create_table(
        "final_results",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column(
            "selected_draft_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "image_path",
            sa.String(length=500),
            nullable=True,
        ),
        sa.Column("saved_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["ad_projects.id"],
        ),
        sa.ForeignKeyConstraint(
            ["selected_draft_id"],
            ["ad_drafts.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_final_results_id",
        "final_results",
        ["id"],
        unique=False,
    )
    op.create_index(
        "ix_final_results_project_id",
        "final_results",
        ["project_id"],
        unique=True,
    )
    op.create_index(
        "ix_final_results_selected_draft_id",
        "final_results",
        ["selected_draft_id"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_final_results_selected_draft_id",
        table_name="final_results",
    )
    op.drop_index(
        "ix_final_results_project_id",
        table_name="final_results",
    )
    op.drop_index(
        "ix_final_results_id",
        table_name="final_results",
    )
    op.drop_table("final_results")

    op.drop_index(
        "ix_ad_strategies_project_id",
        table_name="ad_strategies",
    )
    op.drop_index(
        "ix_ad_strategies_id",
        table_name="ad_strategies",
    )
    op.drop_table("ad_strategies")

    op.drop_index(
        "ix_ad_drafts_project_id",
        table_name="ad_drafts",
    )
    op.drop_index(
        "ix_ad_drafts_id",
        table_name="ad_drafts",
    )
    op.drop_table("ad_drafts")

    op.drop_index(
        "ix_ad_projects_user_id",
        table_name="ad_projects",
    )
    op.drop_index(
        "ix_ad_projects_product_id",
        table_name="ad_projects",
    )
    op.drop_index(
        "ix_ad_projects_id",
        table_name="ad_projects",
    )
    op.drop_table("ad_projects")

    op.drop_index(
        "ix_products_user_id",
        table_name="products",
    )
    op.drop_index(
        "ix_products_id",
        table_name="products",
    )
    op.drop_table("products")

    op.drop_index(
        "ix_users_email",
        table_name="users",
    )
    op.drop_index(
        "ix_users_id",
        table_name="users",
    )
    op.drop_table("users")