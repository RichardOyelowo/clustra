"""added 'full_name' not 'username'

Revision ID: 63deb7ff47a8
Revises: 47f771dd55b4
Create Date: 2026-07-14 18:15:41.245478
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "63deb7ff47a8"
down_revision: Union[str, Sequence[str], None] = "47f771dd55b4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # Add color to tasklabels.
    op.add_column(
        "tasklabels",
        sa.Column("color", sa.String(), nullable=True),
    )

    op.execute(
        """
        UPDATE tasklabels
        SET color = ''
        """
    )

    op.alter_column(
        "tasklabels",
        "color",
        nullable=False,
    )

    # Rename username -> full_name while preserving existing data.
    op.alter_column(
        "users",
        "username",
        new_column_name="full_name",
        existing_type=sa.VARCHAR(length=60),
    )


def downgrade() -> None:
    """Downgrade schema."""

    # Rename full_name back to username.
    op.alter_column(
        "users",
        "full_name",
        new_column_name="username",
        existing_type=sa.VARCHAR(length=60),
    )

    # Remove color from tasklabels.
    op.drop_column("tasklabels", "color")
