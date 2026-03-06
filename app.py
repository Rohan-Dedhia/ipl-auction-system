from flask import Flask,render_template,request,redirect,flash
from database import engine,SessionLocal
from models import Player,Base,User

from flask_login import LoginManager,login_user,login_required,logout_user,current_user
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key="auction_secret"

bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view="login"

Base.metadata.create_all(bind=engine)


@login_manager.user_loader
def load_user(user_id):

    db=SessionLocal()
    user=db.query(User).get(int(user_id))
    db.close()
    return user


@app.route("/",methods=["GET","POST"])
@login_required
def index():

    db=SessionLocal()

    if request.method=="POST":

        player_id=int(request.form["player_id"])
        team=request.form["team"]
        bid=int(request.form["bid"])

        player=db.query(Player).filter(Player.id==player_id).first()

        if player.team==team:
            flash("Same team cannot bid consecutively","error")

        elif bid<=player.current_bid:
            flash("Bid must be higher than current bid","error")

        else:
            player.current_bid=bid
            player.team=team
            db.commit()
            flash("Bid successful","success")

        return redirect("/")

    search=request.args.get("search")
    role=request.args.get("role")

    query=db.query(Player)

    if search:
        query=query.filter(Player.name.ilike(f"%{search}%"))

    if role:
        query=query.filter(Player.role==role)

    players=query.order_by(Player.id).all()

    db.close()

    return render_template("index.html",players=players)


@app.route("/player/<int:id>")
@login_required
def player(id):

    db=SessionLocal()
    player=db.query(Player).filter(Player.id==id).first()
    db.close()

    return render_template("player.html",player=player)


@app.route("/signup",methods=["GET","POST"])
def signup():

    db=SessionLocal()

    if request.method=="POST":

        username=request.form["username"]
        password=request.form["password"]

        hashed=bcrypt.generate_password_hash(password).decode("utf-8")

        user=User(username=username,password=hashed)

        db.add(user)
        db.commit()

        flash("Account created","success")

        return redirect("/login")

    return render_template("signup.html")


@app.route("/login",methods=["GET","POST"])
def login():

    db=SessionLocal()

    if request.method=="POST":

        username=request.form["username"]
        password=request.form["password"]

        user=db.query(User).filter(User.username==username).first()

        if user and bcrypt.check_password_hash(user.password,password):
            login_user(user)
            return redirect("/")

        flash("Invalid login","error")

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():

    logout_user()
    return redirect("/login")


if __name__=="__main__":
    app.run(debug=True)