from datetime import datetime
import os
import time

from dotenv import load_dotenv
import feedparser
import requests
import yaml

load_dotenv()

webhook_id = os.getenv('WEBHOOK_ID')
webhook = f"https://discordapp.com/api/webhooks/{webhook_id}"

frequency = {}
frequency['update'] = 60  # seconds - checking for new posts
frequency['post'] = 10  # seconds - posting between each feed

# DEBUG
DEBUG = False

if DEBUG:
    frequency['update'] = 1
    frequency['post'] = 1


def RSSparser(url):
    '''Fetches newest RSS article and posts it to a discord webhook url.
    '''
    rss = feedparser.parse(url)
    # Most recent article
    u = rss.entries[0]

    rsstitle = rss.feed.get('title', 'No title')

    current_time = time.time()
    current_timestamp = datetime.fromtimestamp(
        current_time
    ).strftime("%A, %B %d, %Y %I:%M:%S")

    # Declare feed dictionary and check for feed elements.
    # This uses the python dictionary get() method to set a value if
    # the element does not exist

    feed = {
        'link':
            u.get('link', 'No link (!)'),
        'date':
            u.get('published', u.get('updated', current_timestamp)),
        'icon': rss.feed.get(
            'icon',
            'https://live.staticflickr.com/3777/10813661054_709581b384_b.jpg'
            ),
        'title':
            u.get('title', 'No title'),
        'desc':
            u.get('summary', 'No description'),
        'content':
            u.get('content', 'No content'),
    }

    # TODO: feed['image']

    payload = {
        'username':
            # This sets the webhook bot's username to the post title.
            feed['title'].split('. ')[0],
        'content':
            # This is the message sent to the discord channel (Markdown works).
            f"{feed['link']} \n",
        'avatar_url':
            # Change this link to customize the webhook bot's avatar picture.
            'https://live.staticflickr.com/3777/10813661054_709581b384_b.jpg'
    }

    print(f"\n{rsstitle}")
    # Get newest article link and compare it to the one saved in the YAML file
    if u.link != urls[url]:
        print(
            "[NEW ARTICLE] "
            "Posting new article: "
            f"'{feed['title']}' to feed '{rsstitle}'"
        )
        urls[url] = u.link
        post = requests.post(webhook, data=payload)
        # DEBUG:
        if DEBUG:
            print(post, feed['link'], '\n')
            print(payload)

        # Update YAML file with new article title
        with open('rss_urls.yaml', 'w') as rss_urls:
            yaml.dump(urls, rss_urls)

    else:
        print(f"[CURRENT] '{rsstitle}' is up to date")

    time.sleep(frequency['post'])


while True:
    with open('rss_urls.yaml') as rss_urls:
        urls = yaml.load(rss_urls, Loader=yaml.FullLoader)

    for url in urls.keys():
        RSSparser(url)
    time.sleep(frequency['update'])
