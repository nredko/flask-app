#!env/bin/python

import feedparser
import urllib2
import re
from BeautifulSoup import BeautifulSoup

from app import model as m, db


def parse_book(url):
    book_id = url[url.rfind('/') + 1:]
    book = m.Book.query.get(book_id)
    if book is not None:
        return book
    html = urllib2.urlopen(url).read()
    parsed_html = BeautifulSoup(html)

    book_title_a = parsed_html.body.find('h1', attrs={'class':'title'}).text
    book_title = book_title_a[:book_title_a.rfind(' ')]

    authors = []
    authors_a = parsed_html.body.findAll('a', attrs={'href':re.compile(r"/a/\d+")})
    for a in authors_a:
        a_id = a['href'][a['href'].rfind('/')+1:]
        author = m.Author.query.get(a_id)
        if author is None:
            author = m.Author(a_id, a.text)
            db.session.add(author)
            db.session.commit()
        authors.append(author)

    genres_a = parsed_html.body.findAll('a', attrs={'class':'genre', 'href':re.compile(r"/g/\d+")})
    genres = []
    for g in genres_a:
        genre_id = g['href'][g['href'].rfind('/')+1:]
        genre = m.Genre.query.get(genre_id)
        if genre is None:
            genre = m.Genre(genre_id, g['name'], g.text)
            db.session.add(genre)
            db.session.commit()
        genres.append(genre)

    print book_id + ': ' +book_title

    book = m.Book(book_id, book_title, authors, genres)
    db.session.add(book)
    db.session.commit()
    return book


db.create_all()
etag_rec = m.Config.query.get('etag')
etag = ''
if etag_rec is not None:
    etag = etag_rec['value']

rss = feedparser.parse('http://flibusta.net/polka/show/all/rss', etag)
if rss.status == 200:
    print rss.etag
    for entry in rss.entries:
        post_id = entry.id[entry.id.rfind('/')+1:]
        if m.Post.query.get(post_id) is None:
            # print entry.title
            book = parse_book(entry.link)
            post = m.Post(post_id, entry.title, entry.summary, book, entry.published_parsed)
            db.session.add(post)
            db.session.commit()
