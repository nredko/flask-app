import os
from flask import render_template, redirect, flash, url_for, send_from_directory
from flask_login import login_required, login_user, current_user, logout_user
from app import *
import model as m
# https://www.openshift.com/blogs/use-flask-login-to-add-user-authentication-to-your-python-application

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/logout/")
def logout_page():
    logout_user()
    return redirect(url_for("/login"))

@app.route("/login/", methods=["GET", "POST"])
@templated()
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        registered_user = User.query.filter_by(username=username, password=hash_pass(password)).first()
        if registered_user is None:
            flash('Username or Password is invalid', 'error')
            return redirect(url_for('login'))
        remember_me = False
        if 'remember-me' in request.form:
            remember_me = True
        login_user(registered_user, remember=remember_me)
        flash('Logged in successfully')
        return redirect(request.args.get('next') or url_for('index'))

@app.route('/register/', methods=['GET', 'POST'])
@templated()
def register():
    if request.method == 'POST':
        user = User(request.form['username'], hash_pass(request.form['password']), request.form['email'])
        db.session.add(user)
        db.session.commit()
        flash('User successfully registered')
        return redirect(url_for('login'))

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
@login_required
def post(post_id=0):
    if post_id != 0:
        return jsonify(post=m.Post.query.get(post_id))
    posts = m.Post.query.order_by(m.Post.pub_date.desc()).all()
    return jsonify(posts=posts)

@app.route("/book/<int:book_id>")
@login_required
def book(book_id):
    return jsonify(book=m.Book.query.get(book_id))

@app.route("/list/")
@login_required
def list():
    user_id = (current_user.get_id() or 0)
    return jsonify(rows=m.List.query(user_id))

@app.route("/read/book/<int:book_id>")
def read_book(book_id=0):
    user_id = current_user.get_id()
    if not user_id:
        return jsonify(result='BAD_LOGIN')
    result=m.mark_read_book(user_id, book_id)
    return jsonify(result='OK '+book_id)

@app.route("/read/posts/<int:book_id>")
def read_posts(book_id=0):
    user_id = current_user.get_id()
    if not user_id:
        return jsonify(result='BAD_LOGIN')
    m.mark_read_posts(user_id, book_id)
    return jsonify(result='OK '+book_id)

