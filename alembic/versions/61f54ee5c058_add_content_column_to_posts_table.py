"""add content column to posts table

Revision ID: 61f54ee5c058
Revises: 4b1850ce9418
Create Date: 2024-01-06 20:38:18.665611

"""
from logging import NullHandler
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '61f54ee5c058'
down_revision: Union[str, None] = '4b1850ce9418'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
