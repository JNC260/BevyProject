/* eslint-disable no-console */
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
const fs = require('fs');
const cheerio = require('cheerio');
const rp = require('request-promise');

const processFeed = function(url){
  const req = request(url);
  const feedparser = new FeedParser();
  req.on('error', function (error) {
    console.log('ERROR=', error);
  });  
  req.on('response', function (res) {
    const stream = this; // `this` is `req`, which is a stream
    if (res.statusCode !== 200) {
        console.log('STATUS=',res.statusCode);
      this.emit('error', new Error('Bad status code'));
    }
    else {
      stream.pipe(feedparser);
    }
  });
  feedparser.on('error', function (error) {
    console.log('ERROR=', error);
    console.log('STATUS=',error.statusCode);
  });
  feedparser.on('readable', function () {
    // This is where the action is!
    const stream = this; // `this` is `feedparser`, which is a stream
    const meta = this.meta; // **NOTE** the "meta" is always available in the context of the feedparser instance
    let item;
         
    while (item = stream.read()) {
      console.log(`${item.title}: ${item.link}`);
    }
  });
};

const options = {
  uri: 'https://www.reddit.com',
  transform: function (body) {
    return cheerio.load(body);
  }
};
  
rp(options)
  .then(($) => {
    // const divs = $('head').find('link[type="text/css"]');
    $('link').each(function(i, elem){
      elem[i] = $(this);
      if(this.attribs.type === 'application/xhtml+xml'|| this.attribs.type === 'application/atom+xml' || this.attribs.type === 'application/rss+xml'){
        console.log(`this might be a feed! here is the link: ${this.attribs.href}`);
      }
      else if(this.attribs.type === undefined){
        console.log('no type');
      }
      else console.log(this.attribs.type);
    });
  })
  .catch((err) => {
    console.log(err);
  });

