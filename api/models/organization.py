from sqlalchemy import Column, String
from .base import Base

class Organization(Base):
    __tablename__ = "organization"
    
    name = Column(String, primary_key=True)
    greek_letters = Column(String)
    type = Column(String)
