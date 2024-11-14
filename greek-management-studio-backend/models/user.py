from sqlalchemy import Column, String, Boolean, ForeignKey
from .base import Base

class User(Base):
    __tablename__ = "user"
    
    email = Column(String, ForeignKey("member.email"), primary_key=True)
    password = Column(String)
    is_admin = Column(Boolean)
