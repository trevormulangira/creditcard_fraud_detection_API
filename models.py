from sqlalchemy import Column, Integer, Numeric, DateTime
from sqlalchemy.sql import func

from database import Base

class Transaction(Base):
    __tablename__ ="transactions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Numeric(12, 2), nullable=False)
    prediction = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now())