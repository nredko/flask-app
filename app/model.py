from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

class Config(db.model):
    param = db.Column(db.String(20), primary_key=True)
    value = db.Column(db.String(120))

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return '<Author %d: %r>' % (self.id, self.name)


class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return '<Genre %d: %r>' % (self.id, self.name)

genres = db.Table('genres',
                db.Column('genre_id', db.Integer, db.ForeignKey('genre.id')),
                db.Column('book_id', db.Integer, db.ForeignKey('book.id'))
)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    author = db.Column(db.Integer, db.ForeignKey('author.id'))
    genres = db.relationship('Genre', secondary=genres,
                       backref=db.backref('genres', lazy='dynamic'))

    def __init__(self, id, name, author, genres):
        self.id = id
        self.author = author
        self.genres = genres
        self.name = name

    def __repr__(self):
        return '<Author %r>' % self.name


class Post(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    title = db.Column(db.String(80))
    body = db.Column(db.Text)
    pub_date = db.Column(db.DateTime)
    user = db.Column(db.String(50))
    book = db.Column(db.Integer,db.ForeignKey('book.id'))
    # category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    # category = db.relationship('Category',
    #     backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, title, body, pub_date=None):
        self.title = title
        self.body = body
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date

    def __repr__(self):
        return '<Post %r>' % self.title