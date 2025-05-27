from sqlalchemy import Column, Integer, String, ForeignKey,Float,Date
from datetime import date
from sqlalchemy.orm import relationship, validates
from db import Base

class Payment(Base):
    __tablename__ = 'payments'
    id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer, ForeignKey('tenants.id'))
    amount = Column(Float, nullable=False)
    date_paid = Column(Date, default=date.today)
    month = Column(String)  # e.g., 'January'
    year = Column(Integer)

    tenant = relationship("Tenant", back_populates="payments")
