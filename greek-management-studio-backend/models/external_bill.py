from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from .base import Base

class ExternalBill(Base):
    __tablename__ = "external_bill"
    
    bill_id = Column(UUID(as_uuid=True), primary_key=True)
    chapter_contact = Column(Integer, ForeignKey("chapter.id"))
    payor_name = Column(String)
    billing_address = Column(String)
    p_email = Column(String)
    p_phone_num = Column(String)
