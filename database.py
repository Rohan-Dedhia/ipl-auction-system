from sqlalchemy import create_engine
from models import Base
import os

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

Base.metadata.create_all(engine)