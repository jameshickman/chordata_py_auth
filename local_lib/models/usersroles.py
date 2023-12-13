from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import declarative_base
from apps.authentication.lib.models.user import User
from apps.authentication.lib.models.roles import Roles
Base = declarative_base()


class UsersRoles(Base):
    __tablename__ = "users_roles"
    __table_args__ = {"schema": "authentication"}
    user = Column(Integer, ForeignKey(User.id))
    role = Column(Integer, ForeignKey(Roles.id))
