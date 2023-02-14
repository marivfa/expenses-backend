"""Add table remainder detail

Revision ID: 3367980d7263
Revises: 31becf5bab72
Create Date: 2023-02-08 18:18:31.958795

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3367980d7263'
down_revision = '31becf5bab72'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'reminders_detail',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('reminder_id', sa.Integer, sa.ForeignKey('remainders.id'), nullable=False),
        sa.Column('date_time', sa.DateTime, nullable=False),
        sa.Column('status', sa.String(length=255), nullable=True),
    )


def downgrade() -> None:
    op.drop_table('reminder_details')
