from sqlalchemy import Column, String
from .base import Base

class School(Base):
    __tablename__ = "school"
    
    name = Column(String, primary_key=True)
    billing_address = Column(String)
