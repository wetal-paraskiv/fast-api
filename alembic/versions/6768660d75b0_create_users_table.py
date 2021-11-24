"""create users table

Revision ID: 6768660d75b0
Revises: a1c64a213538
Create Date: 2021-11-24 11:10:53.073927

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6768660d75b0'
down_revision = 'a1c64a213538'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade():
    op.drop_table('users')
    pass
