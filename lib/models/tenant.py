from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, validates
from db import Base

class Tenant(Base):
    __tablename__ = 'tenants'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    phone = Column(String)
    email = Column(String)
    unit_id = Column(Integer, ForeignKey('units.id'))  # Remove unique=True

    unit = relationship("Unit", back_populates="tenants")
    payments = relationship("Payment", back_populates="tenant")
