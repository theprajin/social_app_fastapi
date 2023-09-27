"""create content column in posts

Revision ID: 02628e8b9cee
Revises: 9651498617b7
Create Date: 2023-09-27 14:08:59.767610

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "02628e8b9cee"
down_revision: Union[str, None] = "9651498617b7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=True))
    pass


def downgrade() -> None:
    op.drop_column("content")
    pass
