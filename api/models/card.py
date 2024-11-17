from sqlalchemy import Column, Integer, String, ForeignKey
from .base import Base

class Card(Base):
    __tablename__ = "card"
    
    payment_id = Column(Integer, ForeignKey("payment_info.payment_id"), primary_key=True)
    card_num = Column(Integer)
    security_code = Column(Integer)
    name = Column(String)
