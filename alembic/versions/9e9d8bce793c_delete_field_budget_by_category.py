"""Delete Field budget by category

Revision ID: 9e9d8bce793c
Revises: fcff65f59a21
Create Date: 2023-03-01 17:42:20.434448

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9e9d8bce793c'
down_revision = 'fcff65f59a21'
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table('category') as batch_op:
        batch_op.drop_column('budget')


def downgrade() -> None:
    with op.batch_alter_table('category') as batch_op:
        batch_op.add_column(
            sa.Column('budget', sa.DECIMAL(10, 2), default=0.00))
