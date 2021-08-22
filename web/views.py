from flask import Blueprint, render_template

views = Blueprint("views", __name__)

@views.route("/")
@views.route("/home")
def home():
    return render_template("main_page.html")

@views.route("/product")
def product():
    return render_template("product_page.html")