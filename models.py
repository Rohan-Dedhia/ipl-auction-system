from sqlalchemy import Column, Integer, String
from database import Base

class Player(Base):

    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    base_price = Column(Integer)
    current_bid = Column(Integer)
    team = Column(String)