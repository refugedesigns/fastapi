from sqlalchemy import Column, Integer, String, Boolean, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from .schemas import RoleEnum
from .database import Base


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="TRUE", nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)  # relationship
    user = relationship("User")  # fetch the user based on the user_id
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), default="user")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class Token(Base):
    __tablename__ = "tokens"
    id = Column(Integer, primary_key=True, nullable=False)
    is_valid = Column(Boolean, server_default="TRUE", nullable=False)
    refresh_token = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)  # relationship
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
