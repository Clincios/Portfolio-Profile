"""Initial schema

Revision ID: 001_initial
Revises:
Create Date: 2026-08-16 22:20:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=50), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_users_id"), ["id"], unique=False)
        batch_op.create_index(batch_op.f("ix_users_username"), ["username"], unique=True)

    op.create_table(
        "profiles",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("title", sa.String(length=150), nullable=False),
        sa.Column("tagline", sa.String(length=255), nullable=False),
        sa.Column("bio_heading", sa.String(length=255), nullable=False),
        sa.Column("bio_paragraph_1", sa.Text(), nullable=False),
        sa.Column("bio_paragraph_2", sa.Text(), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("location", sa.String(length=150), nullable=False),
        sa.Column("resume_url", sa.String(length=500), nullable=False),
        sa.Column("github_url", sa.String(length=500), nullable=False),
        sa.Column("linkedin_url", sa.String(length=500), nullable=False),
        sa.Column("twitter_url", sa.String(length=500), nullable=False),
        sa.Column("typing_roles", sa.String(length=500), nullable=False),
        sa.Column("years_experience", sa.Integer(), nullable=False),
        sa.Column("projects_shipped", sa.Integer(), nullable=False),
        sa.Column("teams_led", sa.Integer(), nullable=False),
        sa.Column("initials", sa.String(length=10), nullable=False),
        sa.Column("contact_heading", sa.String(length=255), nullable=False),
        sa.Column("contact_text", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("profiles", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_profiles_id"), ["id"], unique=False)

    op.create_table(
        "skill_categories",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=100), nullable=False),
        sa.Column("icon", sa.String(length=20), nullable=False),
        sa.Column("sort_order", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("skill_categories", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_skill_categories_id"), ["id"], unique=False)

    op.create_table(
        "skills",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("category_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("sort_order", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["category_id"], ["skill_categories.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("skills", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_skills_id"), ["id"], unique=False)

    op.create_table(
        "experiences",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("date_range", sa.String(length=100), nullable=False),
        sa.Column("role", sa.String(length=150), nullable=False),
        sa.Column("company", sa.String(length=150), nullable=False),
        sa.Column("details", sa.JSON(), nullable=False),
        sa.Column("sort_order", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("experiences", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_experiences_id"), ["id"], unique=False)

    op.create_table(
        "projects",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("category", sa.String(length=50), nullable=False),
        sa.Column("tech_stack", sa.JSON(), nullable=False),
        sa.Column("image_label", sa.String(length=200), nullable=False),
        sa.Column("image_url", sa.String(length=500), nullable=False),
        sa.Column("demo_url", sa.String(length=500), nullable=False),
        sa.Column("demo_label", sa.String(length=100), nullable=False),
        sa.Column("source_url", sa.String(length=500), nullable=False),
        sa.Column("source_label", sa.String(length=100), nullable=False),
        sa.Column("sort_order", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("projects", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_projects_category"), ["category"], unique=False)
        batch_op.create_index(batch_op.f("ix_projects_id"), ["id"], unique=False)

    op.create_table(
        "education",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("degree", sa.String(length=200), nullable=False),
        sa.Column("school", sa.String(length=200), nullable=False),
        sa.Column("year", sa.String(length=50), nullable=False),
        sa.Column("sort_order", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("education", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_education_id"), ["id"], unique=False)

    op.create_table(
        "contact_messages",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("subject", sa.String(length=200), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("is_read", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("(CURRENT_TIMESTAMP)"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("contact_messages", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_contact_messages_id"), ["id"], unique=False)


def downgrade() -> None:
    with op.batch_alter_table("contact_messages", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_contact_messages_id"))
    op.drop_table("contact_messages")

    with op.batch_alter_table("education", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_education_id"))
    op.drop_table("education")

    with op.batch_alter_table("projects", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_projects_id"))
        batch_op.drop_index(batch_op.f("ix_projects_category"))
    op.drop_table("projects")

    with op.batch_alter_table("experiences", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_experiences_id"))
    op.drop_table("experiences")

    with op.batch_alter_table("skills", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_skills_id"))
    op.drop_table("skills")

    with op.batch_alter_table("skill_categories", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_skill_categories_id"))
    op.drop_table("skill_categories")

    with op.batch_alter_table("profiles", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_profiles_id"))
    op.drop_table("profiles")

    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_users_username"))
        batch_op.drop_index(batch_op.f("ix_users_id"))
    op.drop_table("users")
