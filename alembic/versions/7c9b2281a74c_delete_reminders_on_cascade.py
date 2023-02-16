"""Delete Reminders on cascade

Revision ID: 7c9b2281a74c
Revises: 5cb13635ab48
Create Date: 2023-02-15 19:28:45.952771

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7c9b2281a74c'
down_revision = '5cb13635ab48'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Update the foreign key constraint to include DELETE CASCADE behavior
    op.drop_constraint("reminders_detail_ibfk_1", "reminders_detail", type_="foreignkey")
    op.create_foreign_key("reminders_detail_ibfk_1", "reminders_detail", "remainders", ["reminder_id"], ["id"], ondelete="CASCADE")


def downgrade() -> None:
    # Remove the foreign key constraint
    op.drop_constraint("reminders_detail_ibfk_1", "reminders_detail")
