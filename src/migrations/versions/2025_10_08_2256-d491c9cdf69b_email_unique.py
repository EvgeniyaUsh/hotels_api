"""email unique

Revision ID: d491c9cdf69b
Revises: 24cf6ae0b50a
Create Date: 2025-10-08 22:56:16.704653

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "d491c9cdf69b"
down_revision: Union[str, Sequence[str], None] = "24cf6ae0b50a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(None, "user", ["email"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, "user", type_="unique")
