from sqlalchemy import Column, Integer, String, ForeignKey,Float,Date
from datetime import date
from sqlalchemy.orm import relationship, validates
from db import Base,SessionLocal

Session=SessionLocal

class Payment(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer, ForeignKey('tenants.id'))
    amount = Column(Float, nullable=False)
    date_paid = Column(Date, default=date.today)
    month = Column(Integer)
    year = Column(Integer)

    tenant = relationship("Tenant", back_populates="payments")

    # === CRUD METHODS ===

    @classmethod
    def create(cls, session: Session, tenant_id: int, amount: float, date_paid: date = None):
        tenant = Tenant.get_by_id(session, tenant_id)
        if not tenant:
            print("Tenant not found.")
            return

        pay_date = date_paid or date.today()
        payment = cls(
            tenant_id=tenant_id,
            amount=amount,
            date_paid=pay_date,
            month=pay_date.month,
            year=pay_date.year
        )
        session.add(payment)
        session.commit()
        print(f"Payment of {amount} recorded for {tenant.name} ({pay_date.strftime('%B %Y')}).")
        return payment

    @classmethod
    def get_all(cls, session: Session):
        return session.query(cls).all()

    @classmethod
    def get_by_id(cls, session: Session, payment_id: int):
        return session.query(cls).filter_by(id=payment_id).first()

    @classmethod
    def get_by_tenant(cls, session: Session, tenant_id: int):
        return session.query(cls).filter_by(tenant_id=tenant_id).order_by(cls.date_paid.desc()).all()

    @classmethod
    def delete(cls, session: Session, payment_id: int):
        payment = cls.get_by_id(session, payment_id)
        if not payment:
            print("Payment not found.")
            return
        session.delete(payment)
        session.commit()
        print(f"Payment ID {payment_id} deleted.")
        return True
