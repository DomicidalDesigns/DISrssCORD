from datetime import datetime
import os
import time

from dotenv import load_dotenv
import feedparser
import requests
import yaml

load_dotenv()

webhook_id = os.getenv('WEBHOOK_ID')

wait = 60  # seconds
webhook = f"https://discordapp.com/api/webhooks/{webhook_id}"


def RSSparser(url):
    rss = feedparser.parse(url)

    u = rss.entries[0]

    current_time = time.time()
    current_timestamp = datetime.fromtimestamp(
        current_time
    ).strftime("%A, %B %d, %Y %I:%M:%S")

    # Set default values for feed attributes
    feed = {
        'link': None,
        'date': current_timestamp,
        'icon':
            'https://live.staticflickr.com/3777/10813661054_709581b384_b.jpg',
        'title': None,
        'desc': None,
        'content': None,
        'img': None
    }

    # Try updating feed attributes
    try:
        feed['link'] = u.link
        feed['date'] = u.published
        feed['icon'] = rss.feed.image.href
        feed['title'] = u.title
        feed['desc'] = u.summary
        feed['content'] = u.content
        feed['img'] = rss.media_thumbnail[0].url

    except AttributeError as e:
        print(f'[MISSING] Feed {e}\n')
        # print(feed)

    payload = {
        'username': rss.feed.title,
        'content': f"**Date:**  ` {feed['date']} ` \n {feed['link']} \n\n ",
        'avatar_url': feed['icon']
    }
    
    print(f"{rss.feed.title}")
    if u.link != urls[url]:
        print(f"[NEW ARTICLE] Posting new article: {u.title} to feed {rss.feed.title}")
        urls[url] = u.link
        requests.post(webhook, data=payload)
        # Update YAML file with new article title for 
        with open('rss_urls.yaml', 'w') as rss_urls:
            yaml.dump(urls, rss_urls)
    else:
        print(f"[CURRENT] {rss.feed.title} is up to date")

while True:
    with open('rss_urls.yaml') as rss_urls:
        urls = yaml.load(rss_urls, Loader=yaml.FullLoader)

    for url in list(urls.keys()):
        RSSparser(url)
    time.sleep(wait)
