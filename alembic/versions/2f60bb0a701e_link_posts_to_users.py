"""link posts to users

Revision ID: 2f60bb0a701e
Revises: 12d736e50ec0
Create Date: 2023-07-26 12:19:25.594238

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '2f60bb0a701e'
down_revision = '12d736e50ec0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("user_id", sa.Integer, nullable=False))
    op.create_foreign_key("posts_users_fk", source_table="posts", referent_table="users", local_cols=["user_id"],
                          remote_cols=["id"], ondelete="CASCADE")


def downgrade() -> None:
    op.drop_constraint("posts_users_fk", table_name="posts")
    op.drop_column("posts", "user_id")
