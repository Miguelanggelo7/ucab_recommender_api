"""create_skills_table

Revision ID: 3fa22c709bb4
Revises: c7ceacf6381d
Create Date: 2023-08-08 00:26:42.599058

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3fa22c709bb4'
down_revision = 'c7ceacf6381d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('skills',
                    sa.Column('id', sa.INTEGER(), sa.Identity(always=True, start=1, increment=1, minvalue=1,
                              maxvalue=32767, cycle=False, cache=1), autoincrement=True, nullable=False),
                    sa.Column('name', sa.VARCHAR(length=255),
                              autoincrement=False, nullable=False),
                    sa.PrimaryKeyConstraint('id', name='skills_pkey')
                    )


def downgrade() -> None:
    op.drop_table("skills")
