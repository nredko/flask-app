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

class Config(db.Model):
    param = db.Column(db.String(20), primary_key=True)
    value = db.Column(db.String(120))

    def __init__(self, param, value):
        self.param = param
        self.value = value

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
    title = db.Column(db.String(80))

    def __init__(self, id, name, title):
        self.id = id
        self.name = name
        self.title = title

    def __repr__(self):
        return '<Genre %d: %r>' % (self.id, self.name)

book_authors = db.Table('book_authors',
                db.Column('book_id', db.Integer, db.ForeignKey('author.id')),
                db.Column('author_id', db.Integer, db.ForeignKey('book.id'))
)

book_genres = db.Table('book_genres',
                db.Column('genre_id', db.Integer, db.ForeignKey('genre.id')),
                db.Column('book_id', db.Integer, db.ForeignKey('book.id'))
)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    authors = db.relationship('Author', secondary=book_authors,
                       backref=db.backref('authors', lazy='dynamic'))
    genres = db.relationship('Genre', secondary=book_genres,
                       backref=db.backref('genres', lazy='dynamic'))

    def __init__(self, id, name, authors, genres):
        self.id = id
        self.authors = authors
        self.genres = genres
        self.name = name

    def __repr__(self):
        return '<Book %d: %r>' % (self.id, self.name)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    body = db.Column(db.Text)
    pub_date = db.Column(db.DateTime)
    user = db.Column(db.String(50))
    book_id = db.Column(db.Integer,db.ForeignKey('book.id'))
    book = db.relationship('Book', backref=db.backref('post', lazy='dynamic'))


    def __init__(self, id, title, body, book, pub_date=None, user = None):
        self.id = id
        self.title = title
        self.book = book
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date
        self.body = body
        self.user = user


    def __repr__(self):
        return '<Post %r>' % self.title