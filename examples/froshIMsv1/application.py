from flask import Flask, render_template, request
import csv

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def register():
    if request.form["name"] == "" or request.form["school"] == "":
        return render_template("failure.html")
    with open("registrants.csv", "a") as file:
        writer = csv.writer(file)
        writer.writerow((request.form["name"], request.form["school"]))

    return render_template("success.html")