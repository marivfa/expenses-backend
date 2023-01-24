"""Add Country Colum to Users

Revision ID: fce4ee388d31
Revises: 22353ba534e9
Create Date: 2023-01-23 17:23:07.974886

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fce4ee388d31'
down_revision = '22353ba534e9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('country', sa.String(10)))


def downgrade() -> None:
    op.drop_column('users', 'country')