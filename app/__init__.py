from datetime import timedelta
import md5

from flask import Flask, request, redirect, render_template, g
from flask_login import (LoginManager, login_required, login_user, 
                         current_user, logout_user, UserMixin)
from itsdangerous import URLSafeTimedSerializer
from functools import wraps
from flask.ext.sqlalchemy import SQLAlchemy
import json, datetime
from model import User
app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

app.secret_key = "#$%&^*(*(((()&*()*()___*($%@#@#$%#!@vl;8op3945tc  5p4"
login_serializer = URLSafeTimedSerializer(app.secret_key)
login_manager = LoginManager()

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        try:
            return obj.tojson()
        except AttributeError:
            try:
                return json.JSONEncoder.default(self, obj)
            except TypeError as err:
                return json.JSONEncoder.default(self, err)

def jsonify(*args, **kwargs):
    return app.response_class(json.dumps(dict(*args, **kwargs), cls=JSONEncoder), mimetype='application/json')

def hash_pass(password):
    salted_password = password + app.secret_key
    return md5.new(salted_password).hexdigest()

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@login_manager.token_loader
def load_token(token):
    max_age = app.config["REMEMBER_COOKIE_DURATION"].total_seconds()
    data = login_serializer.loads(token, max_age=max_age)
    user = User.get(data[0])
    if user and data[1] == user.password:
        return user
    return None

@app.before_request
def before_request():
    g.user = current_user

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


def exec_sql(sql, params):
    result = db.session.execute(sql, params)
    db.session.commit()
    if not result.return_rows():
        return
    ret = [dict(x) for x in result]
    return ret



app.config["USERS"] = ((1, "admin", hash_pass("123")), ("", ""))
app.config["REMEMBER_COOKIE_DURATION"] = timedelta(days=14)
login_manager.login_view = "/login/"
login_manager.init_app(app)

import views

