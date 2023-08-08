"""create_user_skills_table

Revision ID: 7d0746594aea
Revises: 3fa22c709bb4
Create Date: 2023-08-08 00:27:21.245272

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7d0746594aea'
down_revision = '3fa22c709bb4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('user_skills',
                    sa.Column('user_id', sa.INTEGER(), nullable=False),
                    sa.Column('skills_id',
                              sa.INTEGER(), nullable=False),
                    sa.ForeignKeyConstraint(['user_id'], [
                                            'users.id'], name='user_skills_fk_user_id', onupdate='CASCADE', ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(['skills_id'], [
                                            'skills.id'], name='user_skills_fk_skills_id', onupdate='CASCADE', ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint(
                        "user_id", "skills_id", name='user_skills_pkey')
                    )


def downgrade() -> None:
    op.drop_table("user_skills")
