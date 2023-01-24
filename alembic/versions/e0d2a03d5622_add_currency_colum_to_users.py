"""Add Currency Colum to Users

Revision ID: e0d2a03d5622
Revises: fce4ee388d31
Create Date: 2023-01-23 17:28:43.392546

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e0d2a03d5622'
down_revision = 'fce4ee388d31'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('currency', sa.String(10)))
    op.alter_column('users', sa.Column('country', sa.String(50)))


def downgrade() -> None:
    op.drop_column('users', 'currency')
    op.drop_column('users', 'country')
