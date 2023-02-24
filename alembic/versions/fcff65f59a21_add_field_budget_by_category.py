"""Add Field budget by category

Revision ID: fcff65f59a21
Revises: 7c9b2281a74c
Create Date: 2023-02-16 20:40:33.638870

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fcff65f59a21'
down_revision = '7c9b2281a74c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('category', sa.Column('budget', sa.DECIMAL(10,2) ,default=0.00))


def downgrade() -> None:
    op.drop_column('category', 'budget')
