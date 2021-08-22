from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def main():
    return render_template('main_page.html')

@app.route("/login")
def login():
    return render_template('login_page.html')

@app.route("/register")
def register():
    return render_template('register_page.html')

@app.route("/profile")
def profile():
    return render_template('profile_page.html')

@app.route("/admin")
def admin():
    return render_template('admin_page.html')