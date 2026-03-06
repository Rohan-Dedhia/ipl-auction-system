from flask import Flask, render_template, request, redirect, flash
from database import engine, SessionLocal
from models import Player, Base

app = Flask(__name__)
app.secret_key = "auction_secret"

Base.metadata.create_all(bind=engine)


@app.route("/", methods=["GET", "POST"])
def index():

    db = SessionLocal()

    if request.method == "POST":

        player_id = int(request.form["player_id"])
        team = request.form["team"]
        bid_amount = int(request.form["bid"])

        player = db.query(Player).filter(Player.id == player_id).first()

        if player:

            if player.team == team:
                flash("❌ Same team cannot bid consecutively!", "error")

            elif bid_amount <= player.current_bid:
                flash("❌ Bid must be higher than current bid!", "error")

            else:
                player.current_bid = bid_amount
                player.team = team
                db.commit()
                flash("✅ Bid placed successfully!", "success")

        db.close()
        return redirect("/")

    players = db.query(Player).order_by(Player.id).all()
    db.close()

    return render_template("index.html", players=players)


if __name__ == "__main__":
    app.run(debug=True)