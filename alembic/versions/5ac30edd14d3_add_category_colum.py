"""Add Category Colum

Revision ID: 5ac30edd14d3
Revises: 8512e3c43ffa
Create Date: 2023-01-23 16:51:35.173013

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5ac30edd14d3'
down_revision = '8512e3c43ffa'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('category', sa.Column('id_user', sa.Integer))


def downgrade() -> None:
    op.drop_column('category', 'id_user')
