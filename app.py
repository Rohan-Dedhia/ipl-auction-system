from flask import Flask,render_template,request,redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Player,Base
import os

app = Flask(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

# THIS CREATES THE TABLE AUTOMATICALLY
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

@app.route("/")
def index():

    db = Session()
    players = db.query(Player).all()

    return render_template("index.html",players=players)


@app.route("/bid/<int:id>",methods=["GET","POST"])
def bid(id):

    db = Session()
    player = db.query(Player).filter(Player.id==id).first()

    if request.method=="POST":

        team = request.form["team"]
        bid = int(request.form["bid"])

        if bid > player.current_bid:

            player.current_bid = bid
            player.team = team
            db.commit()

        return redirect("/")

    return render_template("bid.html",player=player)


if __name__=="__main__":
    app.run(debug=True)