# coding=utf-8
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
import json
from sqlalchemy.ext.declarative import declarative_base as real_declarative_base
from sqlalchemy.sql import text
from app import db
import strings as s


def exec_sql(sql, params):
    result = db.session.execute(sql, params)
    if not result.returns_rows:
        db.session.commit()
        return
    ret = [dict(x) for x in result]
    return ret

# Let's make this a class decorator
declarative_base = lambda cls: real_declarative_base(cls=cls)

@declarative_base
class Base(object):
    __exclude__ = ()

    @property
    def columns(self):
        return [ c.name for c in self.__table__.columns ]

    @property
    def columnitems(self):
        dic = {}
        keys = self._sa_instance_state.attrs.items()
        for k, field in keys:
            if k in self.__exclude__:
                continue
            dic[k] = getattr(self, k)
        return dic

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.columnitems)

    def tojson(self):
        return self.columnitems


class User(db.Model, Base):
    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(20), unique=True , index=True)
    password = db.Column('password', db.String(10))
    email = db.Column('email',db.String(50),unique=True , index=True)
    registered = db.Column('registered', db.DateTime)

    def __init__(self , username ,password , email):
        self.username = username
        self.password = password
        self.email = email
        self.registered = datetime.utcnow()

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.username)


class Config(db.Model, Base):
    param = db.Column(db.String(20), primary_key=True)
    value = db.Column(db.String(120))

    def __init__(self, param, value):
        self.param = param
        self.value = value


class Author(db.Model, Base):
    __exclude__ = ('authors')
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return '<Author %d: %r>' % (self.id, self.name)


class Genre(db.Model, Base):
    __exclude__ = ('genres')
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
                db.Column('book_id', db.Integer, db.ForeignKey('book.id')),
                db.Column('author_id', db.Integer, db.ForeignKey('author.id'))
    )

book_genres = db.Table('book_genres',
                db.Column('genre_id', db.Integer, db.ForeignKey('genre.id')),
                db.Column('book_id', db.Integer, db.ForeignKey('book.id'))
    )


class Book(db.Model, Base):
    __exclude__ = ('post')

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

class Post(db.Model, Base):
    __exclude__ = ()
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    body = db.Column(db.Text)
    pub_date = db.Column(db.DateTime)
    user = db.Column(db.String(50))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
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

read_post = db.Table('read_post',
                db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
                db.UniqueConstraint('user_id', 'post_id', name='uix_1'))

read_book = db.Table('read_book',
                db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                db.Column('book_id', db.Integer, db.ForeignKey('book.id')),
                db.UniqueConstraint('user_id', 'book_id', name='uix_1'))

read_author = db.Table('read_author',
                db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                db.Column('author_id', db.Integer, db.ForeignKey('author.id')),
                db.UniqueConstraint('user_id', 'author_id', name='uix_1'))


def get_list(user_id):
    return exec_sql(s.sql_select_posts, {'user_id': user_id})


def mark_read_book(user_id, book_id):
    exec_sql(s.sql_mark_read_book, {'user_id': user_id, 'book_id': book_id})


def mark_read_post(user_id, book_id):
    exec_sql(s.sql_mark_read_post, {'user_id': user_id, 'book_id': book_id})


def mark_read_author(user_id, book_id):
    exec_sql(s.sql_mark_read_author, {'user_id': user_id, 'book_id': book_id})


def mark_unread_post(user_id, book_id):
    exec_sql(s.sql_mark_unread_post, {'user_id': user_id, 'book_id': book_id})


def mark_unread_book(user_id, book_id):
    exec_sql(s.sql_mark_unread_book, {'user_id': user_id, 'book_id': book_id})

def mark_unread_author(user_id, book_id):
    exec_sql(s.sql_mark_unread_author, {'user_id': user_id, 'book_id': book_id})
