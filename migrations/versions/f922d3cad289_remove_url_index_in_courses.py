"""Remove_url_index_in_courses

Revision ID: f922d3cad289
Revises: 7268bdb7ab71
Create Date: 2023-09-17 16:39:12.822406

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f922d3cad289'
down_revision = '7268bdb7ab71'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_constraint("uq_courses_url", "courses")


def downgrade():
    op.create_unique_constraint('uq_courses_url', 'courses', ['url'])
