"""add unique constraint

Revision ID: ab254d3ffbaa
Revises: 6f0524197838
Create Date: 2026-04-24 22:59:03.830593
"""

from typing import Sequence, Union

from alembic import op


revision: str = "ab254d3ffbaa"
down_revision: Union[str, Sequence[str], None] = "6f0524197838"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(
        "uq_hotel_title_location",
        "hotel",
        ["title", "location"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "uq_hotel_title_location",
        "hotel",
        type_="unique",
    )
