from sqlalchemy import Column, Integer, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from .base import Base

class Bill(Base):
    __tablename__ = "bill"
    
    chapter_id = Column(Integer, ForeignKey("chapter.id"))
    bill_id = Column(UUID(as_uuid=True), primary_key=True)
    amount = Column(Float)
    amount_paid = Column(Float)
    due_date = Column(DateTime)
    issue_date = Column(DateTime)
    is_external = Column(Boolean)
