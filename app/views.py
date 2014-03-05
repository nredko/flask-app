from flask import render_template, redirect, flash
from flask_login import login_required, login_user, current_user, logout_user
from app import *
import model as m

@app.route("/logout/")
def logout_page():
    logout_user()
    return redirect("/")

@app.route("/login/", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        user = User.get(request.form['username'])
        if user and hash_pass(request.form['password']) == user.password:
            login_user(user, remember=True)
            return redirect(request.args.get("next") or "/")        
        flash('Bad username or password')
    return render_template("login.html")

@app.route("/")
@templated()
def index():
    user_id = (current_user.get_id() or "No User Logged In")
    return dict(user_id=user_id)

@app.route("/restricted/")
@login_required
@templated()
def restricted():
    user_id = (current_user.get_id() or "No User Logged In")
    return dict(user_id=user_id)

@app.route("/posts/")
@app.route("/post/<int:post_id>")
#@login_required
def post(post_id=0):
    if post_id != 0:
        return jsonify(post=m.Post.query.get(post_id))
    posts = m.Post.query.order_by(m.Post.pub_date.desc()).all()
    return jsonify(posts=posts)

@app.route("/book/<int:book_id>")
#@login_required
def book(book_id):
    return jsonify(book=m.Book.query.get(book_id))

@app.route("/list/")
#@login_required
def list():
    return jsonify(list=m.List.query())
