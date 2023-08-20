"""Add_users_token_column

Revision ID: 5f8400185d6e
Revises: d1104186ea97
Create Date: 2023-08-20 17:58:41.969760

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5f8400185d6e'
down_revision = 'd1104186ea97'
branch_labels = None
depends_on = None


def upgrade():

    op.add_column("users", sa.Column("session_token", sa.Text, default=None))


def downgrade():
    op.drop_column("users", "session_token")
