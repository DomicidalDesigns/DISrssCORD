# DISrssCORD
#### A simple python script to send posts from multiple rss feeds to a discord channel via webhook 
## Description

*(rss in DISCORD)*: a very simple and easy to use RSS feed posting script that works via magic. Well, webhooks and python.

## Dependencies
* **Requests**
* **feedparser**
* **dotenv**
* **PyYAML**

## How to Use
First setup a webhook for your discord server. Learn how to do that [here.](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks)

Clone or download this repo and edit `env.example`. Change `YOUR-WEBHOOK-ID` to whatever the rest of your webhook link looks like.

Include everything after `https://discordapp.com/api/webhooks/`.
If your link was `https://discordapp.com/api/webhooks/123456789/NotARealLink/` then your .env file would look like: ```WEBHOOK_ID=123456789/NotARealLink```

Rename `env.example` to `.env`
**Do not share this file with anyone. Do not put this file in version control. Anyone with this link can post anything they want to your discord server.**

Open up your favorite console and run `python DISrssCORD.py`

## How to Add Feeds
Simply add a URL to the end of the rss_urls.yaml file and add a colon after the url `https://www.wired.com/feed/category/science/latest/rss:`

## What's up with the YAML file?
The YAML file is a dictionary with the URL of the RSS feed as the key and the last posted article URL as the value. This ensures you aren't posting the same article over and over. The script compares the newest article link to the link saved in the YAML file. Previously I used a text file for each RSS feed and just listed the RSS links inside the python file, but that was way messier and required restarting the program to add new URLs. This way you can easily add RSS feeds and it keeps everything in one simple file.
