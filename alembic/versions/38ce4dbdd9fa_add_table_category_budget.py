"""Add Table category-budget

Revision ID: 38ce4dbdd9fa
Revises: 9e9d8bce793c
Create Date: 2023-03-01 17:45:22.534895

"""
from email.policy import default
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '38ce4dbdd9fa'
down_revision = '9e9d8bce793c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'category_budget',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('category_id', sa.Integer, sa.ForeignKey(
            'category.id'), nullable=False),
        sa.Column('user_id', sa.Integer, sa.ForeignKey(
            'users.id'), nullable=False),
        sa.Column('budget', sa.DECIMAL(10, 2), default=0.00, nullable=True),
    )


def downgrade() -> None:
    op.drop_table('category_budget')
