# Welcome to FindFeed!

## Introduction

FindFeed determines if a url contains a syndication feed and processes that feed.

If a feed is found, FindFeed will print out the title, url, and sentiment of each post in the feed along with the positive and negative indicators used to determine the sentiment.

##### Sample Response
```
---------------------------------------------------------------------------
Title: This drone is cleaning windows 1,100 feet above the ground, so
humans don't have to

URL: https://mashable.com/video/window-washing-drones-aerones-cleaning-
turbines/

Positive Indicator Words:
['right', 'kind']

Negative Indicator Words:
['dangerous']

The overall sentiment of this post is neutral!
---------------------------------------------------------------------------
```

If a feed is not found, FindFeed will alert the user.

##### Sample Response
```
No feed found on this site. Try another!
'End'
```

If FindFeed is unable to determine if a feed is present due to a '403 Forbidden' error, FindFeed will alert the user.

##### Sample Response
```
'Sorry! Not authorized to check for feeds on this site.'
'End'
```

## Requirements

* Python version 3
* pip modules:
   * Requests `pip install requests` 
   * TextBlob `pip install textblob`
   * BeautifulSoup  `pip install beautifulsoup`
   * TextWrap `pip install textwrap`

## Setup

1. Clone this repo into the folder of your choice.

`$ git clone https://github.com/JNC260/BevyProject.git`

2. Open the command line.

3. Move into the the repo.

`$ cd BevyProject/`

4. Run the following command with the url you'd like to test.

`$ python findfeed.py <you url>`

   * NOTE: All urls must begin with http:// or https://