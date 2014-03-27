# https://www.openshift.com/blogs/use-flask-login-to-add-user-authentication-to-your-python-application

from flask_login import (LoginManager, login_required, login_user,
                         current_user, logout_user, UserMixin)

from model import User

from app import login_manager, login_serializer, hash_pass
from flask import current_app as app

login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@login_manager.token_loader
def load_token(token):
    max_age = app.config["REMEMBER_COOKIE_DURATION"].total_seconds()
    data = login_serializer.loads(token, max_age=max_age)
    user = User.query.get(data[0])
    if user and data[1] == hash_pass(user.password):
        return user
    return None

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

login_manager.login_view = "/login/"
login_manager.init_app(app)