"""Edit Remainder Column

Revision ID: 3499a4289656
Revises: 1b6ff8b9a86a
Create Date: 2022-12-26 14:40:44.668472

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3499a4289656'
down_revision = '1b6ff8b9a86a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column('remainders', sa.Column('remainder_date', sa.String(50)))

def downgrade() -> None:
    op.alter_column('remainders', 'remainder_date')
