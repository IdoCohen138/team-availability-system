from sqlalchemy import Column, Integer, String
from .database import Base


class User(Base):
     __tablename__ = "users"
     id = Column(Integer, primary_key=True, index=True)
     username = Column(String(50), unique=True, index=True, nullable=False)
     full_name = Column(String(100), nullable=False)
     password_hash = Column(String(256), nullable=False)
     status = Column(String(30), nullable=False, default="Working")