from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base
Base = declarative_base()


class Oauth2(Base):
    __tablename__ = "oauth"
    __table_args__ = {"schema": "authentication"}
    provider = Column(String(128), primary_key=True)
    client_id = Column(String(255))
    secret = Column(String(255))
    redirect = Column(String(255))
