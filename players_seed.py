from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Player
import os

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

db = Session()

players = [
    Player(name="Virat Kohli",base_price=20000000,current_bid=20000000,team=""),
    Player(name="Rohit Sharma",base_price=18000000,current_bid=18000000,team=""),
    Player(name="MS Dhoni",base_price=15000000,current_bid=15000000,team="")
]

db.add_all(players)
db.commit()