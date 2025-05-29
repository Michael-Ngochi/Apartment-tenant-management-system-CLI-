import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../lib")))

from datetime import date
from db import SessionLocal, Base, engine
from models.block import Block
from models.unit import Unit
from models.tenant import Tenant
from models.payment import Payment

session = SessionLocal()

# === Reset DB ===
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

# === Blocks A, B, C ===
block_a = Block(name="A")
block_b = Block(name="B")
block_c = Block(name="C")
session.add_all([block_a, block_b, block_c])
session.flush()

# === Units ===
units = [
    Unit(number="101", block_id=block_a.id),
    Unit(number="102", block_id=block_a.id),
    Unit(number="103", block_id=block_a.id),
    Unit(number="201", block_id=block_b.id),
    Unit(number="202", block_id=block_b.id),
    Unit(number="301", block_id=block_c.id),
    Unit(number="302", block_id=block_c.id),
]
session.add_all(units)
session.flush()

# === Tenants ===
tenants = [
    Tenant(name="Mary Njeri", phone="0711223344", email="marynjeri@gmail.com", unit_id=units[0].id),
    Tenant(name="Kevin Otieno", phone="0722334455", email="kevin.otieno@yahoo.com", unit_id=units[1].id),
    Tenant(name="Sandra Wambui", phone="0711556677", email="sandrawambui@gmail.com", unit_id=units[1].id),
    Tenant(name="James Mwangi", phone="0733112233", email="jamesmwangi@outlook.com", unit_id=units[3].id),
    Tenant(name="Faith Chebet", phone="0700778899", email="faithchebet@gmail.com", unit_id=units[4].id),
    Tenant(name="Brian Kiprotich", phone="0720112233", email="bkiprotich@gmail.com", unit_id=units[5].id),
]
session.add_all(tenants)
session.flush()

# Mark occupied units
for unit in [units[0], units[1], units[3], units[4], units[5]]:
    unit.is_occupied = True

# === Payments (Assume it's May 2025) ===
payments = [
    Payment(tenant_id=tenants[0].id, amount=15000, date_paid=date(2025, 5, 2), month=5, year=2025),
    Payment(tenant_id=tenants[1].id, amount=7500, date_paid=date(2025, 5, 3), month=5, year=2025),
    Payment(tenant_id=tenants[2].id, amount=7500, date_paid=date(2025, 5, 3), month=5, year=2025),
 
    Payment(tenant_id=tenants[4].id, amount=15000, date_paid=date(2025, 5, 4), month=5, year=2025),
    Payment(tenant_id=tenants[5].id, amount=13000, date_paid=date(2025, 5, 5), month=5, year=2025),
]
session.add_all(payments)

session.commit()
session.close()

print("Seed data added: blocks, units, tenants, and payments.")
