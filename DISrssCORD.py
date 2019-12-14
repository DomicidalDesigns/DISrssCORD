import requests
import feedparser
import time

wh_init = "https://discordapp.com/api/webhooks/"
wh_url = wh_init + "WH ID THING GOES HERE"

def RSSparser(url):
    rss=feedparser.parse(url)

    try:
        f_out=open(rss.feed.title+'-posted-feeds.txt','r')
    except IOError:
        print("File not accessible. Creating file.")
        f_out=open(rss.feed.title+'-posted-feeds.txt','w')
        f_out.close()
    finally:
        f_out.close()

    f_out=open(rss.feed.title+'-posted-feeds.txt','r')
    f=f_out.read()
    f=f.strip()

    u=rss.entries[0]

    try:
        link=u.link
    except:
        link = "Link could not be retrieved. (Uh oh)"
        #title=u.title
    try:
        date=u.published
    except:
        date="Date could not be retrieved."
        #desc=u.summary
        #content=u.content
    try:
        icon=rss.feed.image.href
    except:
        icon="https://live.staticflickr.com/3777/10813661054_709581b384_b.jpg"
    #img=rss.media_thumbnail[0].url

    payload={
        'username':rss.feed.title,
        'content':'**Date:** '+'`'+date+'`'+'\n'+link+'\n\n ',
        'avatar_url':icon
        }
    print("Up to date:",u.title == f)
    if u.title != f:
        print("Posting new article:",u.title, "to feed ", rss.feed.title)
        r = requests.post(wh_url,data=payload)
        f_out.close()
        f_out=open(rss.feed.title+'-posted-feeds.txt','w')
        f_out.write(u.title)
    f_out.close()
while True: # URLs go here vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
    for url in [
    'http://rss.sciam.com/ScientificAmerican-News',
    'http://feeds.arstechnica.com/arstechnica/science',
    'https://www.sciencedaily.com/rss/top/science.xml',
    'https://www.technologyreview.com/topnews.rss',
    'https://www.wired.com/feed/category/science/latest/rss',
    'https://www.reddit.com/r/science/.rss',
    'https://www.space.com/feeds/all',
    'http://www.sciencemag.org/rss/news_current.xml',
    'http://feeds.nature.com/nature/rss/current',
    ]:
        RSSparser(url)
    time.sleep(5)
