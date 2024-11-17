from sqlalchemy import Column, String, Integer, ForeignKey
from .base import Base

class Chapter(Base):
    __tablename__ = "chapter"
    
    id = Column(Integer, primary_key=True)
    billing_address = Column(String)
    org_name = Column(String, ForeignKey("organization.name"))
    school_name = Column(String, ForeignKey("school.name"))
