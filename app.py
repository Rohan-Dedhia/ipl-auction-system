from flask import Flask, render_template, request, redirect
from database import engine, SessionLocal
from models import Player, Base

app = Flask(__name__)

Base.metadata.create_all(bind=engine)


@app.route("/", methods=["GET", "POST"])
def index():

    db = SessionLocal()

    if request.method == "POST":

        player_id = int(request.form["player_id"])
        team = request.form["team"]
        bid_amount = int(request.form["bid"])

        player = db.query(Player).filter(Player.id == player_id).first()

        # Check if team already owns another player
        team_exists = db.query(Player).filter(Player.team == team).first()

        if team_exists:
            db.close()
            return "This team already owns a player!"

        if player and bid_amount > player.current_bid:
            player.current_bid = bid_amount
            player.team = team
            db.commit()

        db.close()
        return redirect("/")

    players = db.query(Player).all()
    db.close()

    return render_template("index.html", players=players)


if __name__ == "__main__":
    app.run(debug=True)