#!/usr/bin/env python

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import logging

from google.appengine.dist import use_library
use_library('django', '1.2')

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

import twitter

from services import FetchTweets


class MainHandler(webapp.RequestHandler):
    def get(self):
        tweets = twitter.get_twitter_search('%23ukbeer', '1')
        self.response.out.write(template.render('index.html', {
            'tweets': tweets,
        }))

application = webapp.WSGIApplication([
    ('/services/fetch_tweets', FetchTweets),
    ('/', MainHandler),
], debug=True)

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
