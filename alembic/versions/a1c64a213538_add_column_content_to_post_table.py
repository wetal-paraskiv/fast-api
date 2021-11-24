"""add column content to post table

Revision ID: a1c64a213538
Revises: 8f135f90fc19
Create Date: 2021-11-24 11:05:51.941579

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1c64a213538'
down_revision = '8f135f90fc19'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
