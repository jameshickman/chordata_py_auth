from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import declarative_base
Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    __table_args__ = {"schema": "authentication"}
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(128))
    email = Column(String(128))
    password_hash = Column(String(256))
    password_salt = Column(String(128))
    dav_password = Column(String(128))
    local_login = Column(Boolean())
    first_name = Column(String(128))
    last_name = Column(String(128))
    phone = Column(String(128))
    organization = Column(String(128))
    active = Column(Boolean())
    created = DateTime
    last_login = DateTime
    reset_hash = Column(String(255))
    reset_timestamp = Column(DateTime)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
