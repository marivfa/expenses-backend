"""Add Table Goal 

Revision ID: 74f6e1bf83a1
Revises: 9fba49d51510
Create Date: 2023-03-01 20:10:53.515832

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '74f6e1bf83a1'
down_revision = '9fba49d51510'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'goal',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('description', sa.String(100), nullable=False),
        sa.Column('user_id', sa.Integer, sa.ForeignKey(
            'users.id'), nullable=False),
        sa.Column('amount_target', sa.DECIMAL(
            10, 2), default=0.00, nullable=False),
        sa.Column('target_date', sa.Date, nullable=False),
        sa.Column('real_date', sa.DateTime, nullable=False)
    )

    op.create_table(
        'goal_detail',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('goal_id', sa.Integer, sa.ForeignKey(
            'goal.id', ondelete='CASCADE'), nullable=False),
        sa.Column('real_date', sa.DateTime, nullable=False),
        sa.Column('amount', sa.DECIMAL(10, 2), default=0.00, nullable=False),
        sa.Column('status', sa.String(length=255), nullable=True),
    )


def downgrade() -> None:
    op.drop_table('goal')
    op.drop_table('goal_detail')
