from flask import Flask,redirect,url_for,render_template,request,session,flash
from datetime import timedelta
from flask_sqlalchemy import sqlalchemy

app= Flask(__name__)
app.secret_key = "abhim"
app.config['SQLALCHEMY_DATABASE_URI'] = ''
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime =timedelta(minutes=10)


db = SQLALchemy(app)
 
@app.route("/")
def home():
    return render_template("base.html")

@app.route("/login", methods=["POST","GET"])
def login():
    if request.method =="POST":
        session.permanent = True
        user= request.form["nm"]
        session["user"] =user
        flash("Login sucessfull")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("You are already logged in")
            return redirect(url_for("user"))

        return render_template("login.html")

@app.route("/user", methods=["POST","GET"])
def user():
    email = None
    if "user" in session:
        user = session["user"]

        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email

        else:
            if "email" in session:
                email = session["email"]
                flash("email is saved")
        return render_template("user.html", email=email)
    else:
        flash("You re not logged in")
        return redirect(url_for("login.html"))


@app.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("email", None)
    flash("logged out", "info")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run()