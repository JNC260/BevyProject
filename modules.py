import requests 
import re
from textblob import TextBlob
from bs4 import BeautifulSoup 
from textwrap import fill
import sys

# display message
def print_message(title, url, positives, negatives, sentiment):
    line1=fill("---------------------------------------------------------------------------\n", width=75)
    line2=fill("Title: {title}".format(title=title), width=75)
    line3=fill("URL: {url}".format(url=url), width=75)
    line4=fill("Positive Indicator Words:", width=75)
    line5=fill("{positives}".format(positives=positives), width=75)
    line6=fill("Negative Indicator Words:", width=75)
    line7=fill("{negatives}".format(negatives=negatives), width=75)
    line8=fill("The overall sentiment of this post is {sentiment}!".format(sentiment=sentiment), width=75)
    line9=fill("---------------------------------------------------------------------------", width=75)
    
    message= line1+'\n\n'+line2+'\n\n'+line3+'\n\n'+line4+'\n'+line5+'\n\n'+line6+'\n'+line7+'\n\n'+line8+'\n\n'+line9
    print(message)

# process description sentiment
def process_sentiment(str):
    description = TextBlob(str)
    if description.sentiment.polarity > 0.15:
        sentiment = 'positive'
    if description.sentiment.polarity < -0.15:
        sentiment = 'negative'
    if description.sentiment.polarity >= -0.15 and description.sentiment.polarity <= 0.15:
        sentiment = 'neutral'
    return sentiment

# find positives and negatives
def process_indicators(str):
    description = TextBlob(str)
    assessments = description.sentiment_assessments.assessments
    positives = []
    negatives = []
    for x in assessments:
        word = x[0][0]
        if x[1] > 0:
            positives.append(word.encode('utf8'))
        if x[1] < 0:
            negatives.append(word.encode('utf8'))
    return {'p': positives, 'n':negatives}

# find rss feed link

# process rss feed
def process_feed(feed_url):
    # soupify
    code = requests.get(feed_url)
    plain = code.text
    soup = BeautifulSoup(plain, features='html.parser')
    posts = soup.find_all(['item', 'entry'])
    # find title to print
    for x in posts:
        title = x.find_all('title')[0].text
    # find url to print  
        if x.find_all('link', {'href': not None}) != []:
            link = x.find_all('link', {'href': not None})
            url = link[0].get('href')
        if x.find_all('guid', {'isPermaLink': 'true'}) != []:
            url = x.find_all('guid')[0].text
        if x.findChildren('feedburner:origlink') != []:
            url = x.findChildren('feedburner:origlink')[0].text
  
    # find description text
        if x.find_all('description') != []:
            description = x.find_all('description')[0].text
        if x.find_all('p') != []:
            description = x.find_all('p')[0].text
        if x.find_all('content') != []:
            description = x.find_all('content')[0].text

        sentiment = process_sentiment(description)
        indicators = process_indicators(description)

        if indicators['p'] == []:
            positives = 'No positive indicators found.'
        else:
            positives = indicators['p']
        if indicators['n'] == []:
            negatives = 'No negative indicators found.'
        else:
            negatives = indicators['n']

        print_message(title, url, positives, negatives, sentiment)

def get_rss_feed(website_url):
    if website_url is None:
        print("URL should not be null")
    if website_url.endswith('/feed') or website_url.endswith('.rss') or website_url.endswith('.atom'):
        process_feed(website_url)
    else:
        source_code = requests.get(website_url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, features="html.parser")
        rss = soup.find_all("link", {"type" : "application/rss+xml"})
        atom = soup.find_all("link", {"type" : "application/atom+xml"})
        xhtml = soup.find_all("link", {"type" : "application/xhtml+xml"})
        atags = soup.find_all('a')
        if rss != []:
            for link in rss:
                href = link.get('href')
                if href.startswith('/'):
                    href = website_url+str(href)
                process_feed(href)
        if atom != []:
            for link in atom:
                href = link.get('href')
                if href.startswith('/'):
                    href = website_url+str(href)
                process_feed(href)
        if xhtml != []:
            for link in xhtml:
                href = link.get('href')
                if href.startswith('/'):
                    href = website_url+str(href)
                process_feed(href)
        if atags != []:
            for atags in atags:
                site = atags.get('href')
                if str(site).find('feed') != -1:
                    if site.startswith('/'):
                        site = website_url+str(site)
                    process_feed(site)
        if rss == [] and atom == [] and xhtml == []:
            print('No feed found on this site. Try another!')