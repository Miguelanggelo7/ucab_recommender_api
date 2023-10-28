"""AddClusterFieldToUser

Revision ID: 9c6a649667fc
Revises: 6449db47a695
Create Date: 2023-10-27 20:46:47.100020

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9c6a649667fc'
down_revision = '6449db47a695'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("users", sa.Column("cluster_id", sa.Integer, default=None))


def downgrade():
    op.drop_column("users", "cluster_id")
