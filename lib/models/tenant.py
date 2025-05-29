from sqlalchemy import Column, Integer, String, ForeignKey,extract
from sqlalchemy.orm import relationship, validates
from db import Base,SessionLocal
from models.unit import Unit
from models.payment import Payment
Session=SessionLocal

class Tenant(Base):
    __tablename__ = 'tenants'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    phone = Column(String)
    email = Column(String)
    unit_id = Column(Integer, ForeignKey('units.id'))

    unit = relationship("Unit", back_populates="tenants")
    payments = relationship("Payment", back_populates="tenant")

    # === CRUD METHODS ===

    @classmethod
    def create(cls, session: Session, name: str, phone: str, email: str, unit_id: int):
        unit = Unit.get_by_id(session, unit_id)
        if not unit:
            print("Unit not found.")
            return

        tenant = cls(name=name, phone=phone, email=email, unit_id=unit_id)
        unit.is_occupied = True
        session.add(tenant)
        session.commit()
        print(f"Tenant '{name}' added to Unit {unit.number}.")
        return tenant

    @classmethod
    def get_all(cls, session: Session):
        return session.query(cls).all()

    @classmethod
    def get_by_id(cls, session: Session, tenant_id: int):
        return session.query(cls).filter_by(id=tenant_id).first()

    @classmethod
    def update_contact(cls, session: Session, tenant_id: int, phone: str = None, email: str = None):
        tenant = cls.get_by_id(session, tenant_id)
        if not tenant:
            print("Tenant not found.")
            return

        if phone:
            tenant.phone = phone
        if email:
            tenant.email = email

        session.commit()
        print(f"📱 Contact info for '{tenant.name}' updated.")
        return tenant

    @classmethod
    def vacate(cls, session: Session, tenant_id: int):
        tenant = cls.get_by_id(session, tenant_id)
        if not tenant:
            print("Tenant not found.")
            return
        unit = tenant.unit
        unit.is_occupied = False

        session.delete(tenant)
        session.commit()
        print(f"Tenant '{tenant.name}' removed. Unit '{unit.number}' is now vacant.")
        return True

    @classmethod
    def delete(cls, session: Session, tenant_id: int):
        tenant = cls.get_by_id(session, tenant_id)
        if not tenant:
            print("Tenant not found.")
            return
        session.delete(tenant)
        session.commit()
        print(f"Tenant '{tenant.name}' deleted.")
        return True
    @classmethod
    def get_defaulters(cls, session: Session, month: int, year: int):
        tenants = session.query(cls).all()
        defaulters = []

        for tenant in tenants:
            paid = session.query(Payment).filter(
                Payment.tenant_id == tenant.id,
                Payment.month == month,
                Payment.year == year
            ).first()
            if not paid:
                defaulters.append(tenant)

        return defaulters