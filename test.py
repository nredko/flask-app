#!env/bin/python

import feedparser
from app import model as m

rss = feedparser.parse('http://flibusta.net/polka/show/all/rss', '" 1393317804"')
if rss.status == 200:
    print rss.feed.title
    print rss.etag
    for entry in rss.entries:
        print entry.title
        post = m.Post(entry.title, entry.summary, entry.published_parsed)
