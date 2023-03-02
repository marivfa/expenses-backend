"""Delete on cascade budget- category

Revision ID: 9fba49d51510
Revises: 38ce4dbdd9fa
Create Date: 2023-03-01 17:59:42.590612

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9fba49d51510'
down_revision = '38ce4dbdd9fa'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Update the foreign key constraint to include DELETE CASCADE behavior
    op.drop_constraint("category_budget_ibfk_1",
                       "category_budget", type_="foreignkey")
    op.create_foreign_key("category_budget_ibfk_1", "category_budget", "category", [
                          "category_id"], ["id"], ondelete="CASCADE")


def downgrade() -> None:
    # Remove the foreign key constraint
    op.drop_constraint("category_budget_ibfk_1", "category_budget")
