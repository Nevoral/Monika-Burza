from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Přihlášení proběhlo úspěšně!", category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Zadané heslo není správné.', category='error')
        else:
            flash('Profil pod tímto emailem neexistuje!', category='error')
    return render_template("login_page.html", user=current_user)

@auth.route("/signup", methods=['GET', 'POST'])
def signUp():
    if request.method == 'POST':
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()

        if email_exists:
            flash('Tento email již někdo používá.', category='error')
        elif username_exists:
            flash('Tahle přezdívka již je zabrána.', category='error')
        elif password1 != password2:
            flash('Hesla se musí shodovat!', category='error')
        elif len(username) < 2:
            flash('Přezdívka je příliš krátká.', category='error')
        elif len(password1) < 6:
            flash('Heslo je příliš krátké.', category='error')
        elif len(email) < 4:
            flash("Tohle není validní emailová adressa.", category='error')
        else:
            admin = "user"
            if email == 'monikachadimova15@gmail.com':
                admin = "admin"
            new_user = User(email=email, username=username, password=generate_password_hash(
                password1, method='sha256'), tel_number="", town="", street="", psc="", status=admin)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Účet vytvořen!')
            return redirect(url_for('views.home'))
    return render_template("register_page.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.home"))