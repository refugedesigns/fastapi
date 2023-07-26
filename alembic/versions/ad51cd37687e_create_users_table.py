"""create users table

Revision ID: ad51cd37687e
Revises: 
Create Date: 2023-07-26 11:42:35.653276

"""
from alembic import op
import sqlalchemy as sa
from app.schemas import RoleEnum

# revision identifiers, used by Alembic.
revision = 'ad51cd37687e'
down_revision = None
branch_labels = None
depends_on = None


# __tablename__ = "users"
#     id = Column(Integer, primary_key=True, nullable=False)
#     email = Column(String, nullable=False, unique=True)
#     password = Column(String, nullable=False)
#     role = Column(Enum(RoleEnum), default="user")
#     created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

def upgrade() -> None:
    op.create_table("users",
                    sa.Column("id", sa.Integer, primary_key=True, nullable=False),
                    sa.Column("email", sa.String, nullable=False, unique=True),
                    sa.Column("password", sa.String, nullable=False),
                    sa.Column("role", sa.Enum("user", "admin", "moderator", name="role_enum"), default="user"),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False,
                              server_default=sa.text('now()')),
                    )


def downgrade() -> None:
    op.drop_table("users")
