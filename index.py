import requests 
import re
from textblob import TextBlob
from bs4 import BeautifulSoup  

def parse_rss_feed(feed_url):
    source_code = requests.get(feed_url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, features="html.parser")
    for item in soup.find_all("item"):
        print(item.find('title').text)
        print(item.find('guid').text)
        blob = str(item.find('description'))
        description = TextBlob(blob)
        if description.sentiment.polarity > 0.15:
            print('This article is positive!')
            assessments = description.sentiment_assessments.assessments
            positives = []
            negatives = []
            for x in assessments:
                word = x[0][0]
                if x[1] > 0:
                    positives.append(word)
                if x[1] < 0: 
                    negatives.append(word)
            print('POSITIVES=', positives)
            print('NEGATIVES=', negatives)
        if(description.sentiment.polarity < -0.15):
            print('This article is negative!')
            print(list(description.sentiment_assessments))
        if(description.sentiment.polarity <= 0.15 and description.sentiment.polarity >= -0.15):
            print('This article is neutral.')
    for entry in soup.find_all("entry"):
        print(entry.find('title').text)
        link = entry.find('link', {"href": not None})
        href = link.get('href')
        print(href)

def get_rss_feed(website_url):
    if website_url is None:
        print("URL should not be null")
    if website_url.endswith('/feed'):
        parse_rss_feed(website_url)
    else:
        source_code = requests.get(website_url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, features="html.parser")
        for link in soup.find_all("link", {"type" : "application/rss+xml"}):
                href = link.get('href')
                if href.startswith('/'):
                    href = website_url+str(href)
                parse_rss_feed(str(href))
        for link in soup.find_all("link", {"type" : "application/atom+xml"}):
                href = link.get('href')
                if href.startswith('/'):
                    href = website_url+str(href)
                parse_rss_feed(str(href))
        for link in soup.find_all("link", {"type" : "application/xhtml+xml"}):
                href = link.get('href')
                if href.startswith('/'):
                    href = website_url+str(href)
                parse_rss_feed(str(href))
        for atags in soup.find_all('a'):
            site = atags.get('href')
            if str(site).find('feed') != -1:
                if site.startswith('/'):
                    site = website_url+str(site)
                parse_rss_feed(str(site))

get_rss_feed("https://mashable.com/")

