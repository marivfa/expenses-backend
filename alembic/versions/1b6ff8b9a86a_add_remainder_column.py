"""Add Remainder Column

Revision ID: 1b6ff8b9a86a
Revises: cbbdd448093d
Create Date: 2022-12-26 14:25:36.114580

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1b6ff8b9a86a'
down_revision = 'cbbdd448093d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('remainders', sa.Column('remainder_date', sa.Date))


def downgrade() -> None:
    op.drop_column('remainders', 'remainder_date')
