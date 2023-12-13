from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
Base = declarative_base()


class Roles(Base):
    __tablename__ = "roles"
    __table_args__ = {"schema": "authentication"}
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32), primary_key=True)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
