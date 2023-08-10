"""create_users_specialization_table

Revision ID: c7ceacf6381d
Revises: 1f3fffca83f6
Create Date: 2023-08-08 00:13:20.381671

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c7ceacf6381d'
down_revision = '1f3fffca83f6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('user_specializations',
                    sa.Column('user_id', sa.INTEGER(), nullable=False),
                    sa.Column('specialization_id',
                              sa.INTEGER(), nullable=False),
                    sa.ForeignKeyConstraint(['user_id'], [
                                            'users.id'], name='user_specializations_fk_user_id', onupdate='CASCADE', ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(['specialization_id'], [
                                            'specializations.id'], name='user_specializations_fk_specialization_id', onupdate='CASCADE', ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint(
                        "user_id", "specialization_id", name='user_specializations_pkey')
                    )


def downgrade() -> None:
    op.drop_table("user_specializations")
