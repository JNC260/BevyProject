//how to determine if URL is a feed itself - what is the format?
//parse html to find ATOM or RSS
//in ATOM or RSS in html, where is the URL? title?
//do I determine the positive/negative indicators? is there a formula for that?
//function that counts indicators then compares to determine mood
//how to run in command line? just console.log?

//THIS USES FEEDPARSER TO GET INFO FROM FEED URLS ONLY
const express = require('express');
const app = express();
const FeedParser = require('feedparser');
const request = require('request');

const processFeed = function(url){
  const req = request(url);
  const feedparser = new FeedParser();
  req.on('error', function (error) {
    console.log('ERROR=', error);
  });  
  req.on('response', function (res) {
    const stream = this; // `this` is `req`, which is a stream
    if (res.statusCode !== 200) {
      this.emit('error', new Error('Bad status code'));
    }
    else {
      stream.pipe(feedparser);
    }
  });
  feedparser.on('error', function (error) {
    console.log('ERROR=', error);
  });
  feedparser.on('readable', function () {
    // This is where the action is!
    var stream = this; // `this` is `feedparser`, which is a stream
    var meta = this.meta; // **NOTE** the "meta" is always available in the context of the feedparser instance
    var item;
         
    while (item = stream.read()) {
      console.log(`${item.title}: ${item.link}`);
    }
  });
};

console.log(processFeed('http://www.tbray.org/ongoing/ongoing.atom'));


