#SeQueL
#SoftDev1 pd1
#p00

from flask import Flask, request, redirect, session, render_template, url_for, flash
import os

app = Flask(__name__)
app.secret_key = os.urandom(32)

username = "user"
password = "password"

@app.route("/", methods=["GET"])
def root():
    if 'user' in session:
        return redirect(url_for("home"))
    else:
        return redirect(url_for("login"))

@app.route("/home", methods=["GET"])
def home():
    return render_template(
        "home.html"
    )

@app.route("/login", methods=["GET","POST"])
def login():
    if(request.method == "GET"):
        return render_template("login.html")
    elif(request.method == "POST"):
        return "post"
    # if(request.method == "POST"):
    #     return "this is a post"
    # elif(request.method == "GET"):
    #     return "this is a get"

@app.route("/register", methods=["GET", "POST"])
def register():
    return "register"

if __name__ == "__main__":
	app.debug = True
	app.run()