"""Edit Remainder type

Revision ID: 8512e3c43ffa
Revises: 3499a4289656
Create Date: 2022-12-26 15:36:18.700003

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8512e3c43ffa'
down_revision = '3499a4289656'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('remainders', sa.Column('repeat', sa.String(50)))


def downgrade() -> None:
    op.drop_column('remainders', 'repeat')

