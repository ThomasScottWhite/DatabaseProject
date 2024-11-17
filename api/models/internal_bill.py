from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from .base import Base

class InternalBill(Base):
    __tablename__ = "internal_bill"
    
    bill_id = Column(UUID(as_uuid=True), primary_key=True)
    member_email = Column(String, ForeignKey("member.email"))
