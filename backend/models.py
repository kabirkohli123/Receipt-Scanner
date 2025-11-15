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
    category = Column(String)

    invoice_number = Column(String, nullable=True)   # <<< ADD THIS
    raw_text = Column(String)
