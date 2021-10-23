from flask import Blueprint, render_template, request, flash, redirect, url_for, Response
from flask_login import login_required, current_user
from .models import Post, User, Burza
from . import db
import fpdf
import os

views = Blueprint("views", __name__)

@views.route("/")
@views.route("/home")
def home():
    posts = Post.query.all()
    posts.reverse()
    for i in posts:
        if i.status:
            posts.remove(i)
    posts = posts[:15]
    return render_template("main_page.html", user=current_user, posts=posts)

@views.route("/create_product/<id>", methods=['GET', 'POST'])
@login_required
def update_product(id):
    if request.method == "POST":
        name = request.form.get("name")
        color = request.form.get("color")
        size = request.form.get("size")
        label = request.form.get("label")
        price = request.form.get("price")
        find_post= Post.query.filter_by(id=id).first()
        username = User.query.filter_by(id=find_post.author).first()
        try:
            if price != "":
                cislo = float(price)
        except:
            flash('Cena musí být číslo', category = 'error')
            return redirect(url_for('views.update_product', id=id))
        if name != "":
            find_post.name = name
        if color != "":
            find_post.color = color
        if size != "":
            find_post.size = size
        if size != "":
            find_post.size = size
        if label != "":
            find_post.label = label
        if price != "":
            find_post.price = price
        db.session.commit()
        flash('Položka vytvořena!', category='success')
        return redirect(url_for('views.posts', username=username.username))

    post = Post.query.filter_by(id=id).first()
    return render_template('create_page.html', user=current_user, post=post)

@views.route("/product/<username>/create_product", methods=['GET', 'POST'])
@login_required
def create_product(username):
    if request.method == "POST":
        name = request.form.get("name")
        color = request.form.get("color")
        size = request.form.get("size")
        label = request.form.get("label")
        price = request.form.get("price")
        if name == "" or color == "" or size == "" or price == "":
            flash('Musíte vyplnit všechna pole označena "*"', category = 'error')
            return redirect(url_for('views.create_product', username=username))
        try:
            cislo = float(price)
        except:
            flash('Cena musí být číslo', category = 'error')
            return redirect(url_for('views.create_product', username=username))
        new_post = Post(bring = False, label = label, name = name, color = color, size = size, price = price, status = False, author=current_user.id)
        db.session.add(new_post)
        db.session.commit()
        flash('Položka vytvořena!', category='success')
        return redirect(url_for('views.posts', username=username))
    user = User.query.filter_by(username=username).first()
    
    if not user:
        flash('Nebyl nalezen uživatel pod tímto jménem.', category='error')
        return redirect(url_for('views.home'))

    return render_template('create_page.html',user=current_user, post = None, username=username)

@views.route("/delete_product/<id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()
    username = User.query.filter_by(id=post.author).first()
    if not post:
        flash("Položka neexistuje.", category='error')
    elif current_user.id != post.author:
        flash('Nemáš oprávnění smazat tuto položku.', category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Položka byla odstraněna.', category='success')

    return redirect(url_for('views.posts', username=username.username))


@views.route("/product/<username>")
@login_required
def posts(username, posts = []):
    user = User.query.filter_by(username=username).first()

    if not user:
        flash('Nebyl nalezen uživatel pod tímto jménem.', category='error')
        return redirect(url_for('views.home'))
    if posts == []:
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
        find_user= User.query.filter_by(username=username).first()
        if email != "":
            find_user.email = email
        if new_username != "":
            find_user.username = new_username
        if tel_number != "":
            find_user.tel_number = tel_number
        if town != "":
            find_user.town = town
        if street != "":
            find_user.street = street
        if psc != "":
            find_user.psc = psc
        db.session.commit()
        return redirect(url_for('views.home'))
    return render_template("profile_page.html", user=current_user, username=username)

@views.route("/delete_sell")
@login_required
def delete_sell():
    posts = Post.query.all()
    for post in posts:
        if post.status:
            posts.remove(post)
    flash('Prodané položky byly schovány.', category='success')
    return redirect(url_for('views.admin', tab = '4'))

@views.route("/unmarked_bring")
@login_required
def unmarked_bring():
    posts = Post.query.all()
    for post in posts:
        if post.status:
            post.status = False
    flash('Neprodané položky byly zpět označené za nepřítomné.', category='success')
    return redirect(url_for('views.admin', tab = '4'))

@views.route("/sold/<id>")
@login_required
def sold(id):
    post = Post.query.filter_by(id=id).first()
    post.status = not post.status
    db.session.commit()
    return render_template("admin_page.html", user=current_user, posts=Post.query.all(), username=current_user.username, tab='2')

@views.route("/admin", methods=['GET', 'POST'])
@login_required
def admin():
    find_posts = Post.query.all()
    if request.method == 'POST':
        if request.form.get('action') == 'buyer':
            id_list = request.form.getlist('checkID')
            if id_list == []:
                return render_template("admin_page.html", user=current_user, posts=find_posts, username=current_user.username, tab='2')
            tot_price = 0
            #hlavička faktury
            for i in id_list:
                post = Post.query.filter_by(id = i).first()
                tot_price += float(post.price)
                if not post:
                    flash("Položka neexistuje", category = 'error')
                else:
                    #prodan0 produktz
                    post.status = True
                    db.session.commit()
            #přidíní celkové částky k zaplacení
            flash('Položky byly označeny za prodané', category='success')
            return render_template("admin_page.html", user=current_user, posts=find_posts, username=current_user.username, tab='2')
        elif request.form.get('action') == 'seller':
            id_user = request.form.get('userID')
            if id_user == "":
                return render_template("admin_page.html", user=current_user, posts=find_posts, username=current_user.username, tab='1')
            user = User.query.filter_by(id = id_user).first()
            posts = user.posts
            tot_price = 0
            #hlavička faktury
            for i in posts:
                post = Post.query.filter_by(id = i).first()
                if post.status:
                    tot_price += float(post.price)
                if not post:
                    flash("Položka neexistuje", category = 'error')
                else:
                    #prodan0 produktz
                    post.bring = False
                    db.session.commit()
            #přidíní celkové částky k zaplacení
            tot_price = tot_price * 0.9
            flash('Položky byly označeny za prodané', category='success')
            return render_template("admin_page.html", user=current_user, posts=find_posts, username=current_user.username, tab='1')
        elif request.form.get('action') == 'bring':
            id_list = request.form.getlist("checkID")
            for i in id_list:
                post = Post.query.filter_by(id=i).first()
                username = User.query.filter_by(id=post.author).first()
                if not post:
                    flash("Položka neexistuje.", category='error')
                else:
                    post.bring = True
                    db.session.commit()
            flash('Položky byly označeny.', category='success')
            return render_template("admin_page.html", user=current_user, posts=find_posts, username=username, tab='1')
        else:
            return render_template("admin_page.html", users=User.query.all(), user=current_user, posts=find_posts, username=current_user.username, tab='4')
    return render_template("admin_page.html", users=User.query.all(), user=current_user, posts=find_posts, username=current_user.username, tab='1')

@views.route("/table_pdf/<username>", methods=['GET', 'POST'])
@login_required
def print_user_table(username):
    if request.method == 'POST':
        id_list = request.form.getlist('checkID')
        user = User.query.filter_by(username=username).first()
        pdf = fpdf.FPDF()
        pdf.add_page()
        page_width = pdf.w - 2 * pdf.l_margin
        pdf.add_font("NotoSans", style="", fname="C:/Users/Intel/Downloads/NotoSans-hinted/NotoSans-Regular.ttf", uni=True)
        if request.form.get('action') == 'tabulka':
            pdf.set_font('NotoSans', '', 18)
            pdf.cell(page_width, 0.0, 'Seznam zboží', align='C')
            pdf.ln(10)
            pdf.set_font('NotoSans', '', 14)
            pdf.cell(24, 0.0, 'Účastnik: ', align='L')
            pdf.cell(50, 0.0, username, align='L')
            pdf.ln(5)
            pdf.cell(17, 0.0, 'Email: ', align='L')
            pdf.cell(50, 0.0, user.email, align='L')
            pdf.ln(5)
            pdf.cell(8, 0.0, 'ID: ', align='L')
            pdf.cell(50, 0.0, str(user.id), align='L')
            pdf.ln(10)
            pdf.set_font('NotoSans', '', 11)
            columnW = page_width/5
            th = pdf.font_size
            th += 3
            pdf.cell(columnW, th, 'ID', border=1, align='L')
            pdf.cell(columnW, th, 'Název', border=1, align='L')
            pdf.cell(columnW, th, 'Barva', border=1, align='L')
            pdf.cell(columnW, th, 'Velikost', border=1, align='L')
            pdf.cell(columnW, th, 'Cena', border=1, align='R')
            pdf.ln(th)
            for i in id_list:
                product = Post.query.filter_by(id=int(i)).first()
                pdf.cell(columnW, th, str(product.id), border=1, align='L')
                pdf.cell(columnW, th, str(product.name), border=1, align='L')
                pdf.cell(columnW, th, str(product.color), border=1, align='L')
                pdf.cell(columnW, th, str(product.size), border=1, align='L')
                pdf.cell(columnW, th, str(product.price), border=1, align='R')
                pdf.ln(th)
            return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=seznam_polozek.pdf'})
        elif request.form.get('action') == 'stitek':
            pdf.set_font('NotoSans', '', 11)
            columnW = page_width/4
            th = pdf.font_size + 3
            k=0
            top = pdf.y
            start = pdf.x
            offset = pdf.x + columnW
            for i in id_list:
                if k == 4:
                    pdf.ln(th)
                    pdf.ln(th)
                    pdf.ln(th)
                    top = pdf.y
                    pdf.x = start
                    offset = start + columnW
                    k = 0
                product = Post.query.filter_by(id=int(i)).first()
                text = 'ID: ' + str(product.id) + '\nVelikost: ' + str(product.size) + '\nCena: ' + str(product.price) + ' Kč'
                pdf.multi_cell(columnW, th, txt = text, border=1, align='J')
                pdf.y = top
                pdf.x = offset
                offset += columnW
                k += 1
            return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=stitky.pdf'})
        else:
            flash('Něco proběhlo špatně, zkuste to znovu.', category='error')
            return redirect(url_for('views.posts', username=username))

@views.route("/fakturaSeller_pdf", methods=['GET', 'POST'])
@login_required
def print_user_faktura():
    if request.method == 'POST':
        userID = request.form.get('userID')
        if userID != "":
            user = User.query.filter_by(id=userID).first()
            pdf = fpdf.FPDF()
            pdf.add_page()
            page_width = pdf.w - 2 * pdf.l_margin
            pdf.add_font("NotoSans", style="", fname="C:/Users/Intel/Downloads/NotoSans-hinted/NotoSans-Regular.ttf", uni=True)
            if request.form.get('action') == 'confirm':
                pdf.set_font('NotoSans', '', 18)
                pdf.cell(page_width, 0.0, 'Faktura', align='C')
                pdf.ln(10)
                pdf.set_font('NotoSans', '', 14)
                pdf.cell(24, 0.0, 'Účastnik: ', align='L')
                pdf.cell(50, 0.0, user.username, align='L')
                pdf.ln(5)
                pdf.cell(17, 0.0, 'Email: ', align='L')
                pdf.cell(50, 0.0, user.email, align='L')
                pdf.ln(5)
                pdf.cell(8, 0.0, 'ID: ', align='L')
                pdf.cell(50, 0.0, str(user.id), align='L')
                pdf.ln(10)
                pdf.set_font('NotoSans', '', 11)
                columnW = page_width/5
                th = pdf.font_size
                th += 3
                pdf.cell(columnW, th, 'ID', border=1, align='L')
                pdf.cell(columnW, th, 'Název', border=1, align='L')
                pdf.cell(columnW, th, 'Barva', border=1, align='L')
                pdf.cell(columnW, th, 'Velikost', border=1, align='L')
                pdf.cell(columnW, th, 'Cena', border=1, align='R')
                pdf.ln(th)
                """ for i in id_list:
                    product = Post.query.filter_by(id=int(i)).first()
                    pdf.cell(columnW, th, str(product.id), border=1, align='L')
                    pdf.cell(columnW, th, str(product.name), border=1, align='L')
                    pdf.cell(columnW, th, str(product.color), border=1, align='L')
                    pdf.cell(columnW, th, str(product.size), border=1, align='L')
                    pdf.cell(columnW, th, str(product.price), border=1, align='R')
                    pdf.ln(th) """
                return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=seznam_polozek.pdf'})
            elif request.form.get('action') == 'stitek':
                pdf.set_font('NotoSans', '', 11)
                columnW = page_width/4
                th = pdf.font_size + 3
                k=0
                top = pdf.y
                start = pdf.x
                offset = pdf.x + columnW
                """ for i in id_list:
                    if k == 4:
                        pdf.ln(th)
                        pdf.ln(th)
                        pdf.ln(th)
                        top = pdf.y
                        pdf.x = start
                        offset = start + columnW
                        k = 0
                    product = Post.query.filter_by(id=int(i)).first()
                    text = 'ID: ' + str(product.id) + '\nVelikost: ' + str(product.size) + '\nCena: ' + str(product.price) + ' Kč'
                    pdf.multi_cell(columnW, th, txt = text, border=1, align='J')
                    pdf.y = top
                    pdf.x = offset
                    offset += columnW
                    k += 1 """
                return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=stitky.pdf'})
            else:
                flash('Něco proběhlo špatně, zkuste to znovu.', category='error')
        else:
            flash('Není vyplněno id uživatele.', category='error')
            return redirect(url_for('views.admin', posts=posts))

@views.route("/bring/<id>")
@login_required
def bring(id):
    post = Post.query.filter_by(id=id).first()
    username = User.query.filter_by(id=post.author).first()
    if not post:
        flash("Položka neexistuje.", category='error')
    elif current_user.id != post.author:
        flash('Nemáš oprávnění označit tuto položku.', category='error')
    else:
        post.bring = not post.bring
        db.session.commit()
        flash('Položka byla označena.', category='success')

    return render_template("admin_page.html", user=current_user, posts=Post.query.all(), username=current_user.username, tab='1')

@views.route("/make_admin/<id>")
@login_required
def make_admin(id):
    user = User.query.filter_by(id=id).first()
    user.status = "admin"
    db.session.commit()
    flash('Hodnost uživatele byla změněna', category='success')
    return render_template("admin_page.html", users=User.query.all(), user=current_user, posts=Post.query.all(), username=current_user.username, tab='4')

@views.route("/make_seller/<id>")
@login_required
def make_seller(id):
    user = User.query.filter_by(id=id).first()
    user.status = "seller"
    db.session.commit()
    flash('Hodnost uživatele byla změněna', category='success')
    return render_template("admin_page.html", users=User.query.all(), user=current_user, posts=Post.query.all(), username=current_user.username, tab='4')

@views.route("/make_user/<id>")
@login_required
def make_user(id):
    user = User.query.filter_by(id=id).first()
    user.status = "user"
    db.session.commit()
    flash('Hodnost uživatele byla změněna', category='success')
    return render_template("admin_page.html", users=User.query.all(), user=current_user, posts=Post.query.all(), username=current_user.username, tab='4')

@views.route("/get-location/<int:id>")
def display_route(id):
    burza = Burza.query.get(id)
    return {"x": burza.xLoc, "y": burza.yLoc}

