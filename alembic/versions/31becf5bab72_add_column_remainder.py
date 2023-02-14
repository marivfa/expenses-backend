"""Add column remainder

Revision ID: 31becf5bab72
Revises: ece476da4e5c
Create Date: 2023-02-08 17:55:39.473551

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '31becf5bab72'
down_revision = 'ece476da4e5c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('remainders', sa.Column('remainder_date', sa.Date))


def downgrade() -> None:
    op.drop_column('remainders', 'remainder_date')
