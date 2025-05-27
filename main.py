import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "lib")))

from db import SessionLocal
from models import Block

blocka=Block("A")