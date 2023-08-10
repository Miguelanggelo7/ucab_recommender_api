"""add_url_and_carrer_courses

Revision ID: a223c6eb525c
Revises: 7d0746594aea
Create Date: 2023-08-10 00:54:33.592606

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a223c6eb525c'
down_revision = '7d0746594aea'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('courses', sa.Column('url', sa.Text, nullable=False))
    op.create_unique_constraint('uq_courses_url', 'courses', ['url'])
    op.add_column('courses', sa.Column('career', sa.String(length=255), nullable=False))

def downgrade():
    op.drop_constraint('uq_coursesurl', 'courses', type='unique')
    op.drop_column('courses', 'url')
    op.drop_column('courses', 'career') 
