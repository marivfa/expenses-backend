"""Add Country Colum to Users

Revision ID: 22353ba534e9
Revises: 9971288501a3
Create Date: 2023-01-23 17:20:41.846003

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '22353ba534e9'
down_revision = '9971288501a3'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.add_column('users', sa.Column('country', sa.String(10)))


def downgrade() -> None:
    op.drop_column('users', 'country')