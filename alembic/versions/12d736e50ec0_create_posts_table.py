"""create posts table

Revision ID: 12d736e50ec0
Revises: ad51cd37687e
Create Date: 2023-07-26 12:15:36.133001

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '12d736e50ec0'
down_revision = 'ad51cd37687e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts',
                    sa.Column("id", sa.Integer, primary_key=True, nullable=False),
                    sa.Column("title", sa.String, nullable=False),
                    sa.Column("content", sa.String, nullable=False),
                    sa.Column("published", sa.Boolean, server_default="TRUE", nullable=False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False,
                              server_default=sa.text('now()')))


def downgrade() -> None:
    op.drop_table("posts")
