from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Post, User
from . import db

views = Blueprint("views", __name__)

@views.route("/")
@views.route("/home")
def home():
    posts = Post.query.all()
    return render_template("main_page.html", user=current_user, posts=posts)

@views.route("/create-products", methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == "POST":
        text = request.form.get('text')

        if not text:
            flash('Post cannot be empty', category='error')
        else:
            post = Post(text=text, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Post created!', category='success')
            return redirect(url_for('views.home'))

    return render_template('create_product.html', user=current_user)


@views.route("/delete-products/<id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()

    if not post:
        flash("Post does not exist.", category='error')
    elif current_user.id != post.id:
        flash('You do not have permission to delete this post.', category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted.', category='success')

    return redirect(url_for('views.posts'))


@views.route("/product/<username>")
@login_required
def posts(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        flash('No user with that username exists.', category='error')
        return redirect(url_for('views.home'))

    posts = user.posts
    return render_template("product_page.html", user=current_user, posts=posts, username=username)

@views.route("/profile/<username>", methods=['GET', 'POST'])
@login_required
def profile(username):
    if request.method == 'POST':
        email = request.form.get("email")
        new_username = request.form.get("username")
        tel_number = request.form.get("tel_number")
        town = request.form.get("town")
        street = request.form.get("street")
        psc = request.form.get("psc")
        if tel_number != "":
            tel_exists = User.query.filter_by(tel_number=tel_number).first()
        else:
            tel_exists = False
        if tel_exists:
            flash('Telefoní číslo už někdo používá.', category='error')
        else:
            find_user= User.query.filter_by(username=username).first()
            if email != "":
                find_user.email = str(email)
            if new_username != "":
                find_user.username = new_username
            if tel_number != "":
                find_user.tel_number = str(tel_number)
            if town != "":
                find_user.town = town
            if street != "":
                find_user.street = street
            if psc != "":
                find_user.psc = psc
            db.session.commit()
    return render_template("profile_page.html", user=current_user, username=username)