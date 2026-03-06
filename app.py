from flask import Flask, render_template, request, redirect
from database import engine, SessionLocal
from models import Player, Base

app = Flask(__name__)

# create tables automatically
Base.metadata.create_all(bind=engine)


@app.route("/")
def index():

    db = SessionLocal()
    players = db.query(Player).all()
    db.close()

    return render_template("index.html", players=players)


@app.route("/bid/<int:id>", methods=["GET", "POST"])
def bid(id):

    db = SessionLocal()
    player = db.query(Player).filter(Player.id == id).first()

    if request.method == "POST":

        team = request.form["team"]
        bid = int(request.form["bid"])

        if bid > player.current_bid:
            player.current_bid = bid
            player.team = team
            db.commit()

        db.close()
        return redirect("/")

    return render_template("bid.html", player=player)


if __name__ == "__main__":
    app.run(debug=True)