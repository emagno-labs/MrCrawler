#!/bin/python3.3.2
# -`*- coding: utf-8 -*-
from core.crawler.twitter_lookup import TwitterLookUp
from core.crawler.twitter_oauth_dance import get_twitter_stream
from core.exceptions.crawl_exceptions import MaxTweetsReachError

class TwitterSearch(TwitterLookUp):
   def search(self, filter_term, max_tweets, wsid, user_id):
      pass
