"""Change date remainder detail

Revision ID: 5cb13635ab48
Revises: 3367980d7263
Create Date: 2023-02-09 19:31:27.502159

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5cb13635ab48'
down_revision = '3367980d7263'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column('reminders_detail', sa.Column('date_time', sa.Date))

def downgrade() -> None:
    op.alter_column('reminders_detail', 'date_time')
