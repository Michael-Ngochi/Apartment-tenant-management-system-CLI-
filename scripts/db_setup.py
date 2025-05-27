import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../lib")))

from db import engine, Base
from models import Block,Unit,Tenant,Payment

# Create tables
Base.metadata.create_all(bind=engine)

print("Tables created successfully.")
