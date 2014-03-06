#!env/bin/python
# -*- coding: utf-8 -*-

import feedparser
import urllib2
import urllib
import re
from BeautifulSoup import BeautifulSoup
from datetime import datetime
import time
from app import model as m, db
from sqlalchemy import exc
from cookielib import CookieJar
try:
    import cPickle as pickle
except ImportError:
    import pickle

class StringCookieJar(CookieJar):
    def __init__(self, string=None, policy=None):
        CookieJar.__init__(self, policy)
        if string:
            self._cookies = pickle.loads(str(string))
    def dump(self):
        return pickle.dumps(self._cookies)


def login():
    cj = StringCookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)
    authentication_url = 'http://flibusta.net/node?destination=node'
    payload = {
        'name': 'Nike000',
        'pass': '715434',
        'persistent_login': '1',
        'form_id': 'user_login_block'
    }
    data = urllib.urlencode(payload)
    req = urllib2.Request(authentication_url, data)
    urllib2.urlopen(req)
    cookie = m.Config.query.get('cookie')
    if cookie is None:
        cookie = m.Config('cookie', cj.dump())
        db.session.add(cookie)
    else:
        cookie.value = cj.dump()
    db.session.commit()
    return cookie


def parse_book(url):
    book_id = url[url.rfind('/') + 1:]
    book = m.Book.query.get(book_id)
    if book is not None:
        return book

    cookie = m.Config.query.get('cookie')
    if cookie is None:
        cookie = login()
    url = 'http://flibusta.net/b/356183'
    cj = StringCookieJar(cookie.value)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)
    html = urllib2.urlopen(url).read()

    parsed_html = BeautifulSoup(html)
    content = parsed_html.body.find('div', attrs={'id':'main'})
    book_title_a = content.find('h1', attrs={'class':'title'}).text
    book_title = book_title_a[:book_title_a.rfind(' ')]

    if book_title == u'Книг':
        cookie.value = None
        db.session.commit()
        login()
        return parse_book(url)

    authors = []
    authors_added = set([])

    authors_a = content.findAll('a', attrs={'href':re.compile(r"/a/\d+")})
    for a in authors_a:
        a_id = a['href'][a['href'].rfind('/')+1:]
        if a_id not in authors_added:
            author = m.Author.query.get(a_id)
            if author is None:
                author = m.Author(a_id, a.text)
                db.session.add(author)
                db.session.commit()
            authors.append(author)
            authors_added.add(a_id)

    genres_a = content.findAll('a', attrs={'class':'genre', 'href':re.compile(r"/g/\d+")})
    genres = []
    genres_added = set([])
    for g in genres_a:
        genre_id = g['href'][g['href'].rfind('/')+1:]
        if genre_id not in genres_added:
            genre = m.Genre.query.get(genre_id)
            if genre is None:
                genre = m.Genre(genre_id, g['name'], g.text)
                db.session.add(genre)
                db.session.commit()
            genres.append(genre)
            genres_added.add(genre_id)

    book = m.Book(book_id, book_title, authors, genres)
    db.session.add(book)
    db.session.commit()
    return book

def login():
    cj = StringCookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)
    authentication_url = 'http://flibusta.net/node?destination=node'
    payload = {
        'name': 'Nike000',
        'pass': '715434',
        'persistent_login': '1',
        'form_id': 'user_login_block'
    }
    data = urllib.urlencode(payload)
    req = urllib2.Request(authentication_url, data)
    urllib2.urlopen(req)
    cookie = m.Config.query.get('cookie')
    if cookie is None:
        cookie = m.Config('cookie', cj.dump())
        db.session.add(cookie)
    else:
        cookie.value = cj.dump()
    db.session.commit()
    return cookie


def load():
    etag_rec = m.Config.query.get('etag')

    if etag_rec is not None:
        etag = etag_rec.value
        pass
    else:
        etag = ''
        etag_rec = m.Config('etag', '')
        db.session.add(etag_rec)
    try:
        rss = feedparser.parse('http://flibusta.net/polka/show/all/rss', etag)
        count = 0
        if rss.status == 200:
            etag = rss.etag
            print datetime.now().strftime('%x %X') + ' ' + rss.etag + ': ',
            for entry in rss.entries:
                post_id = entry.id[entry.id.rfind('/')+1:]
                if m.Post.query.get(post_id) is None:
                    book = parse_book(entry.link)
                    body = entry.summary
                    r = re.compile(r' ... ')
                    pos = r.search(body)
                    user = body[:pos.regs[0][0]]
                    body[body.find('\n') + 1:]
                    post = m.Post(post_id, entry.title, entry.summary.replace('\n', '<br />'), book, datetime.fromtimestamp(time.mktime(entry.published_parsed)), user)
                    try:
                        db.session.add(post)
                        db.session.commit()
                        count += 1
                    except exc.SQLAlchemyError as ex:
                        db.session.rollback()
                        print ex
                else:
                    pass
            print count
            etag_rec.value = etag
            db.session.commit()
    except Exception as e:
        print e
        pass

db.create_all()
while True:
    load()
    time.sleep(30)