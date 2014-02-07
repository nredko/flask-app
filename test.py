#!env/bin/python

import feedparser
from app import model as m
rss = feedparser.parse('http://flibusta.net/polka/show/all/rss', '"1391600766"')
if rss.status == 200:
    print rss.feed.title
    for entry in rss.entries:
        print entry.title
        post = m.Post(entry.title, entry.summary, entry.published_parsed)
