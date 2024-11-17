from sqlalchemy import Column, Integer, String, ForeignKey
from .base import Base

class BankAccount(Base):
    __tablename__ = "bank_account"
    
    payment_id = Column(Integer, ForeignKey("payment_info.payment_id"), primary_key=True)
    account_num = Column(Integer)
    routing_num = Column(Integer)
