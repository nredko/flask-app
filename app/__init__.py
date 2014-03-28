from flask import Flask, request, render_template, g, abort
#from flask_login import
from functools import wraps
from flask.ext.sqlalchemy import SQLAlchemy
import json, datetime
from flask.ext.login import LoginManager, current_user
from itsdangerous import URLSafeTimedSerializer
from hashlib import sha256

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])


def hash_pass(password):
    salted_password = password + app.config["SECRET_KEY"]
    return sha256(salted_password).hexdigest()


@app.before_request
def before_request():
    g.user = current_user
    g.user_id = current_user.get_id()


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


def restricted(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user_id is None:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

import login
import views




