"""Add column remainder day

Revision ID: ece476da4e5c
Revises: aaba8170e8c4
Create Date: 2023-02-08 17:49:23.219718

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ece476da4e5c'
down_revision = 'aaba8170e8c4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('remainders', sa.Column('remainder_date', sa.Date))

def downgrade() -> None:
    op.add_column('remainders', 'remainder_date')
