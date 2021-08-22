from flask import Blueprint, render_template

auth = Blueprint("auth", __name__)

@auth.route("/login")
def login():
    return render_template("login_page.html")

@auth.route("/signup")
def signUp():
    return render_template("register_page.html")

@auth.route("/logout")
def logout():
    return "Logout"