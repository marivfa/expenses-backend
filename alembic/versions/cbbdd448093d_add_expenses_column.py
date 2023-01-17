"""Add Expenses Column

Revision ID: cbbdd448093d
Revises: 
Create Date: 2022-12-20 12:22:32.010931

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cbbdd448093d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('expenses', sa.Column('real_date', sa.Date))
    op.add_column('expenses', sa.Column('comment',sa.String(200)))


def downgrade() -> None:
    op.drop_column('expenses', 'real_date')
    op.drop_column('expenses', 'comment')
