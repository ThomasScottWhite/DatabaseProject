from sqlalchemy import Column, Integer, String, ForeignKey
from .base import Base

class PaymentInfo(Base):
    __tablename__ = "payment_info"
    
    member_email = Column(String, ForeignKey("member.email"))
    payment_id = Column(Integer, primary_key=True)
    nickname = Column(String)
