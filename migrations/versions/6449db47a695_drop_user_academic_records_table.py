"""drop_user_academic_records_table

Revision ID: 6449db47a695
Revises: 99c171327574
Create Date: 2023-09-18 00:22:18.572286

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6449db47a695'
down_revision = '99c171327574'
branch_labels = None
depends_on = None


def upgrade():
    # op.drop_table("user_academic_records")
    pass


def downgrade() -> None:
    pass
