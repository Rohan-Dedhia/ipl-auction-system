from sqlalchemy import Column,Integer,String,Float
from database import Base
from flask_login import UserMixin


class Player(Base):

    __tablename__ = "players"

    id = Column(Integer,primary_key=True)
    name = Column(String)
    role = Column(String)
    nationality = Column(String)
    batting_style = Column(String)
    bowling_style = Column(String)

    runs = Column(Integer)
    strike_rate = Column(Float)

    base_price = Column(Integer)
    current_bid = Column(Integer)
    team = Column(String)


class User(Base,UserMixin):

    __tablename__="users"

    id = Column(Integer,primary_key=True)
    username = Column(String,unique=True)
    password = Column(String)