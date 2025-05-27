import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../lib")))

from sqlalchemy.orm import Session
from datetime import date, timedelta
import random
from faker import Faker

from db import engine, SessionLocal, Base
from models import Block, Unit, Tenant, Payment

fake = Faker()

# Create tables if not already created
Base.metadata.create_all(bind=engine)
session = SessionLocal()

# === Blocks ===
block_names = ['A', 'B', 'C', 'D', 'E', 'F']
blocks = [Block(name=name) for name in block_names]
session.add_all(blocks)
session.flush()  # assign block IDs

# === Units ===
units = []
for block in blocks:
    for floor in range(1, 7):  # 6 floors
        for room in range(1, 7):  # 6 rooms per floor
            number = int(f"{floor}0{room}")  # e.g., 101, 204
            unit = Unit(number=str(number), block_id=block.id)
            units.append(unit)

session.add_all(units)
session.flush()  # assign unit IDs

# === Tenants ===
num_tenants = 50
tenant_objs = []
occupied_units = random.sample(units, num_tenants)

for i in range(num_tenants):
    name = fake.name()
    phone = fake.phone_number()
    email = fake.email()
    unit = occupied_units[i]
    unit.is_occupied = True

    tenant = Tenant(name=name, phone=phone, email=email, unit_id=unit.id)
    tenant_objs.append(tenant)

session.add_all(tenant_objs)
session.flush()

# === Payments ===
payments = []

for tenant in tenant_objs:
    num_payments = random.randint(1, 3)
    for i in range(num_payments):
        months_back = random.randint(0, 5)
        pay_date = date.today() - timedelta(days=30 * months_back)
        payment = Payment(
            tenant_id=tenant.id,
            amount=random.choice([12000, 13000, 15000, 17000]),
            date_paid=pay_date,
            month=pay_date.month,
            year=pay_date.year
        )
        payments.append(payment)

session.add_all(payments)

# === Finalize ===
session.commit()
session.close()

print("Substantial seed data inserted successfully.")
