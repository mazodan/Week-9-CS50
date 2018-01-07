from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///froshims3.db"
app.config["SQLALCHEMY_ECHO"] = True
db = SQLAlchemy(app)

class Registrant(db.Model):
    __tablename__ = 'registrants'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.Text)
    school = db.Column(db.Text)

    def __init__(self, name, school):
        self.name = name
        self.school = school

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def register():
    if request.form["name"] == "" or request.form["school"] == "":
        return render_template("failure.html")
    registrant = Registrant(request.form["name"], request.form["school"])
    db.session.add(registrant)
    db.session.commit()
    return render_template("success.html")

@app.route("/registrants")
def registrants():
    rows = Registrant.query.all()
    return render_template("registrants.html", rows = rows)

@app.route("/unregister", methods=["GET", "POST"])
def unregister():
    if request.method == "GET":
        rows = Registrant.query.all()
        return render_template("unregister.html", rows = rows)
    elif request.method == "POST":
        if request.form['id']:
            Registrant.query.filter(Registrant.id == request.form['id']).delete()
            db.session.commit()
        return redirect(url_for("registrants"))