"""create_user_likes_table

Revision ID: 99c171327574
Revises: f922d3cad289
Create Date: 2023-09-17 23:55:29.035826

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '99c171327574'
down_revision = 'f922d3cad289'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("user_likes",
                    sa.Column("user_id", sa.INTEGER(), nullable=False),
                    sa.Column("course_id", sa.INTEGER(), nullable=False),
                    sa.ForeignKeyConstraint(["user_id"], [
                                            "users.id"], name="user_likes_fk_user_id", onupdate='CASCADE', ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(["course_id"], [
                                            "courses.id"], name="user_likes_fk_course_id", onupdate='CASCADE', ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint(
                        "user_id", "course_id", name='user_likes_pkey')
                    )


def downgrade():
    op.drop_table("user_likes")
