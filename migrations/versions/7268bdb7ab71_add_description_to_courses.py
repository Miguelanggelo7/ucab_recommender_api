"""Add_Description_To_Courses

Revision ID: 7268bdb7ab71
Revises: 2da4b05dc6fb
Create Date: 2023-09-17 16:26:52.197269

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7268bdb7ab71'
down_revision = '2da4b05dc6fb'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("courses", sa.Column("description", sa.Text, default=None))


def downgrade():
    op.drop_column("courses", "description")
