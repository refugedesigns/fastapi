"""create tokens table

Revision ID: 08ec1b5b0ce4
Revises: 2f60bb0a701e
Create Date: 2023-07-26 12:23:55.457299

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '08ec1b5b0ce4'
down_revision = '2f60bb0a701e'
branch_labels = None
depends_on = None


# __tablename__ = "tokens"
#     id = Column(Integer, primary_key=True, nullable=False)
#     is_valid = Column(Boolean, server_default="TRUE", nullable=False)
#     refresh_token = Column(String, nullable=False)
#     user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)  # relationship
#     created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

def upgrade() -> None:
    op.create_table("tokens",
                    sa.Column("id", sa.Integer, nullable=False),
                    sa.Column("is_valid", sa.Boolean, nullable=False, server_default="TRUE"),
                    sa.Column("refresh_token", sa.String, nullable=False),
                    sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False,
                              server_default=sa.text('now()')),
                    sa.PrimaryKeyConstraint("id"),
                    )


def downgrade() -> None:
    op.drop_table("tokens")
