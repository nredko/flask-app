# coding=utf-8
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
from app import db
import json
from sqlalchemy.ext.declarative import declarative_base as real_declarative_base

# Let's make this a class decorator
declarative_base = lambda cls: real_declarative_base(cls=cls)

@declarative_base
class Base(object):
    """
    Add some default properties and methods to the SQLAlchemy declarative base.
    """
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

    # @property
    # def columnitems(self):
    #     return dict([ (c, getattr(self, c)) for c in self.columns ])

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.columnitems)

    def tojson(self):
        return self.columnitems

class User(db.Model, Base):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

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

class List():
    sql = (
        u'select count(post.id) count, b.*, c.dt date, Group_Concat(\'<div>\'||post.body||\'</div>\',\'<hr>\') body from (select book.*, authors from '
        u'book left join (select book_id, Group_Concat(SUBSTR(\' \'||name,1+length(rtrim(\' \'||name, '
        u'\'ЁЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮёйцукенгшщзхъфывапролджэячсмитьбю'
        u'QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm`1234567890-=~!@#$%^&*()_+|",./<>?\'))) '
        u') authors from book_authors join author on author_id = author.id group by book_id) a on book.id = a.book_id '
        u') b join (select book_id, max(pub_date) as dt from post group by book_id) c on  b.id = c.book_id join post on '
        u'post.book_id = b.id group by b.id order by c.dt desc'
    )
