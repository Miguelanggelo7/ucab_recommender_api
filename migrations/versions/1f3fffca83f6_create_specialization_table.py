"""create_specialization_table

Revision ID: 1f3fffca83f6
Revises: d42a94e8e408
Create Date: 2023-08-08 00:08:20.169643

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1f3fffca83f6'
down_revision = 'd42a94e8e408'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('specializations',
                    sa.Column('id', sa.INTEGER(), sa.Identity(always=True, start=1, increment=1, minvalue=1,
                              maxvalue=32767, cycle=False, cache=1), autoincrement=True, nullable=False),
                    sa.Column('name', sa.VARCHAR(length=255),
                              autoincrement=False, nullable=False),
                    sa.PrimaryKeyConstraint('id', name='specializations_pkey')
                    )


def downgrade() -> None:
    op.drop_table("specializations")
