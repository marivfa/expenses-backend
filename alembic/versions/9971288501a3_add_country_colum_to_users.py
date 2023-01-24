"""Add Country Colum to Users

Revision ID: 9971288501a3
Revises: 5ac30edd14d3
Create Date: 2023-01-23 17:16:37.657619

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9971288501a3'
down_revision = '5ac30edd14d3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column('users', sa.Column('country', sa.String(10)))


def downgrade() -> None:
    op.drop_column('users', 'country')
