#!env/bin/python

import feedparser
import urllib2
import re
from BeautifulSoup import BeautifulSoup

from app import model as m

rss = feedparser.parse('http://flibusta.net/polka/show/all/rss', '" 1393317804"')


def parse_book(url):
    book_id = url[url.rfind('/') + 1:]
    html = urllib2.urlopen(url).read()
    parsed_html = BeautifulSoup(html)
    book_title = parsed_html.body.find('h1', attrs={'class':'title'}).text
    book_title = book_title[:book_title.rfind(' ')]
    author_a = parsed_html.body.find('a', attrs={'href':re.compile(r"/a/\d+")})
    author_name = author_a.text
    author_id = author_a.attrMap['href'][author_a.attrMap['href'].rfind('/')+1:]
    book_title = book_title[:book_title.rfind(' ')]
    print book_id + ': ' +book_title
    print '   '+author_id + ': ' + author_name
    author = m.Author(author_id, author_name)
    book = m.Book(id, title, author, genres)


if rss.status == 200:
    print rss.feed.title
    print rss.etag
    for entry in rss.entries:
        # print entry.title
        parse_book(entry.link)
        # post = m.Post(entry.title, entry.summary, entry.published_parsed)

