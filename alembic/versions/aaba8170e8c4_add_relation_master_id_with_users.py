"""Add Relation master_id with Users

Revision ID: aaba8170e8c4
Revises: e0d2a03d5622
Create Date: 2023-01-31 21:22:44.037616

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aaba8170e8c4'
down_revision = 'e0d2a03d5622'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column('users', sa.Column('master_id', sa.Integer, sa.ForeignKey('users.id'), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'master_id')
