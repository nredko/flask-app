#!env/bin/python

import feedparser

rss = feedparser.parse('http://flibusta.net/polka/show/all/rss', '"1391600766"')
if rss.status == 200:
    print rss.feed.title
    for entry in rss.entries:
        print entry.title
