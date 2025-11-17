from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Receipt(Base):
    __tablename__ = "receipts"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    vendor = Column(String)
    date = Column(String)
    amount = Column(Float)
    invoice_number = Column(String)
    raw_text = Column(String)

    # ADD THESE NEW FIELDS
    tax = Column(Float, nullable=True)
    payment_method = Column(String, nullable=True)  
    category = Column(String, nullable=True)


