"""change_date_to_string_courses

Revision ID: d1104186ea97
Revises: a223c6eb525c
Create Date: 2023-08-10 02:18:21.074836

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd1104186ea97'
down_revision = 'a223c6eb525c'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('courses', 'begin_date',
                    existing_type=sa.Date(), type_=sa.String())
    op.alter_column('courses', 'end_date',
                    existing_type=sa.Date(), type_=sa.String())


def downgrade():
    op.alter_column('courses', 'begin_date',
                    existing_type=sa.String(), type_=sa.Date())
    op.alter_column('courses', 'end_date',
                    existing_type=sa.String(), type_=sa.Date())
