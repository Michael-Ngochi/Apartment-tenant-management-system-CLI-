from sqlalchemy import Column, Integer, String, ForeignKey,Boolean
from sqlalchemy.orm import relationship, validates
from db import Base


class Unit(Base):
    __tablename__ = 'units'
    id = Column(Integer, primary_key=True)
    number = Column(String, nullable=False)
    block_id = Column(Integer, ForeignKey('blocks.id'))
    is_occupied = Column(Boolean, default=False)

    block = relationship("Block", back_populates="units")
    tenants = relationship("Tenant", back_populates="unit")