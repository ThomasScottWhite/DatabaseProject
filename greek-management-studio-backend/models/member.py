from sqlalchemy import Column, String, Integer, Date, Boolean, ForeignKey
from .base import Base

class Member(Base):
    __tablename__ = "member"
    
    chapter_id = Column(Integer, ForeignKey("chapter.id"))
    email = Column(String, primary_key=True)
    fname = Column(String)
    lname = Column(String)
    dob = Column(Date)
    member_id = Column(Integer)
    member_status = Column(String)
    is_chapter_admin = Column(Boolean)
    phone_num = Column(String)
