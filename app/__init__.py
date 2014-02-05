from datetime import timedelta
import md5

from flask import Flask, request, redirect, render_template
from flask_login import (LoginManager, login_required, login_user, 
                         current_user, logout_user, UserMixin)
from itsdangerous import URLSafeTimedSerializer
from functools import wraps
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

app.secret_key = "#$%&^*(*(((()&*()*()___*($%@#@#$%#!@vl;8op3945tc  5p4"
login_serializer = URLSafeTimedSerializer(app.secret_key)
login_manager = LoginManager()

class User(UserMixin):
    def __init__(self, userid, password):
        self.id = userid
        self.password = password

    def get_auth_token(self):
        data = [str(self.id), self.password]
        return login_serializer.dumps(data)

    @staticmethod
    def get(userid):
        for user in app.config["USERS"]:
            if user[0] == userid:
                return User(user[0], user[1])
        return None

def hash_pass(password):
    salted_password = password + app.secret_key
    return md5.new(salted_password).hexdigest()

@login_manager.user_loader
def load_user(userid):
    return User.get(userid)

@login_manager.token_loader
def load_token(token):
    max_age = app.config["REMEMBER_COOKIE_DURATION"].total_seconds()
    data = login_serializer.loads(token, max_age=max_age)
    user = User.get(data[0])
    if user and data[1] == user.password:
        return user
    return None

def templated(template=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            template_name = template
            if template_name is None:
                template_name = request.endpoint \
                    .replace('.', '/') + '.html'
            ctx = f(*args, **kwargs)
            if ctx is None:
                ctx = {}
            elif not isinstance(ctx, dict):
                return ctx
            return render_template(template_name, **ctx)
        return decorated_function
    return decorator

app.config["USERS"] = (("admin", hash_pass("123")), ("", ""))
app.config["REMEMBER_COOKIE_DURATION"] = timedelta(days=14)
login_manager.login_view = "/login/"
login_manager.init_app(app)

import views

