"""Create_graduate_users_table

Revision ID: 2da4b05dc6fb
Revises: 5f8400185d6e
Create Date: 2023-09-11 23:56:50.363141

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2da4b05dc6fb'
down_revision = '5f8400185d6e'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "graduate_users",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True)
    )

    op.create_table(
        "graduate_user_specializations",
        sa.Column('graduate_user_id', sa.INTEGER(), nullable=False),
        sa.Column('specialization_id',
                  sa.INTEGER(), nullable=False),
        sa.ForeignKeyConstraint(['graduate_user_id'], [
                                'graduate_users.id'], name='graduate_user_specializations_fk_graduate_user_id', onupdate='CASCADE', ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['specialization_id'], [
                                'specializations.id'], name='graduate_user_specializations_fk_specializations_id', onupdate='CASCADE', ondelete='CASCADE'),
        sa.PrimaryKeyConstraint(
            "graduate_user_id", "specialization_id", name='graduate_user_specializations_pkey')
    )

    op.create_table(
        "graduate_user_skills",
        sa.Column('graduate_user_id', sa.INTEGER(), nullable=False),
        sa.Column('skill_id',
                  sa.INTEGER(), nullable=False),
        sa.ForeignKeyConstraint(['graduate_user_id'], [
                                'graduate_users.id'], name='graduate_user_skills_fk_graduate_user_id', onupdate='CASCADE', ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['skill_id'], [
                                'skills.id'], name='graduate_user_skills_fk_skills_id', onupdate='CASCADE', ondelete='CASCADE'),
        sa.PrimaryKeyConstraint(
            "graduate_user_id", "skill_id", name='graduate_user_skills_pkey')
    )


def downgrade():
    op.drop_table("graduate_user_skills")
    op.drop_table("graduate_user_specializations")
    op.drop_table("graduate_users")
