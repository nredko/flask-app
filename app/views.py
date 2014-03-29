import os
from flask import g, redirect, flash, url_for, send_from_directory
from flask_login import login_required, login_user, logout_user
from app import *
import model as m

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/logout/")
def logout_page():
    logout_user()
    return redirect(url_for("login"))


@app.route("/login/", methods=["GET", "POST"])
@templated()
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        registered_user = m.User.query.filter_by(username=username, password=hash_pass(password)).first()
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
        user = m.User(request.form['username'], hash_pass(request.form['password']), request.form['email'])
        db.session.add(user)
        db.session.commit()
        flash('User successfully registered')
        return redirect(url_for('login'))


@app.route("/")
@login_required
@templated()
def index():
    return dict(user_id=g.user_id)


@app.route("/book/<int:book_id>")
@restricted
def book(book_id):
    return jsonify(book=m.Book.query.get(book_id))


@app.route("/list/")
@restricted
def get_list():
    return jsonify(rows=m.get_list(g.user_id))


@app.route("/read/book/<int:book_id>")
@restricted
def read_book(book_id):
    m.mark_read_book(g.user_id, book_id)
    return jsonify(result='OK '+str(book_id))


@app.route("/read/post/<int:book_id>")
@restricted
def read_post(book_id):
    m.mark_read_post(g.user_id, book_id)
    return jsonify(result='OK '+str(book_id))


@app.route("/read/author/<int:book_id>")
@restricted
def read_author(book_id):
    m.mark_read_author(g.user_id, book_id)
    return jsonify(result='OK '+str(book_id))


@app.route("/unread/book/<int:book_id>")
@restricted
def unread_book(book_id):
    m.mark_unread_book(g.user_id, book_id)
    return jsonify(result='OK '+str(book_id))


@app.route("/unread/posts/<int:book_id>")
@restricted
def unread_posts(book_id):
    m.mark_unread_post(g.user_id, book_id)
    return jsonify(result='OK '+str(book_id))


@app.route("/unread/author/<int:book_id>")
@restricted
def unread_author(book_id):
    m.mark_unread_author(g.user_id, book_id)
    return jsonify(result='OK '+str(book_id))
