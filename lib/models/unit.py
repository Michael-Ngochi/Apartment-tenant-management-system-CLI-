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
    tenants = relationship("Tenant", back_populates="unit")  # if many tenants per unit

    # === CRUD METHODS ===

    @classmethod
    def create(cls, session: Session, number: str, block_id: int):
        unit = cls(number=number, block_id=block_id)
        session.add(unit)
        session.commit()
        print(f"Unit '{number}' created under Block ID {block_id}.")
        return unit

    @classmethod
    def get_all(cls, session: Session):
        return session.query(cls).all()

    @classmethod
    def get_by_id(cls, session: Session, unit_id: int):
        return session.query(cls).filter_by(id=unit_id).first()

    @classmethod
    def get_vacant_units(cls, session: Session):
        return session.query(cls).filter_by(is_occupied=False).all()

    @classmethod
    def assign_tenant(cls, session: Session, unit_id: int):
        unit = cls.get_by_id(session, unit_id)
        if not unit:
            print("Unit not found.")
            return
        if unit.is_occupied:
            print("Unit is already occupied.")
            return
        unit.is_occupied = True
        session.commit()
        print(f"Unit '{unit.number}' marked as occupied.")
        return unit

    @classmethod
    def vacate(cls, session: Session, unit_id: int):
        unit = cls.get_by_id(session, unit_id)
        if not unit:
            print("Unit not found.")
            return
        unit.is_occupied = False
        session.commit()
        print(f"Unit '{unit.number}' marked as vacant.")
        return unit

    @classmethod
    def delete(cls, session: Session, unit_id: int):
        unit = cls.get_by_id(session, unit_id)
        if not unit:
            print("Unit not found.")
            return
        session.delete(unit)
        session.commit()
        print(f"Unit '{unit.number}' deleted.")
        return True