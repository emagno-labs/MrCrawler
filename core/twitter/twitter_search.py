#!/bin/python3.3.2
# -`*- coding: utf-8 -*-
from core.twitter.twitter_lookup import TwitterLookUp, MAX_TWEETS_FOR_FIND_OUT
from core.twitter.twitter_oauth_dance import get_twitter_api
from core.exceptions.crawl_exceptions import MaxTweetsReachError

from core.twitter.utils import das_tretas_vish

class TwitterSearch(TwitterLookUp):
   def search(self, wsid):
      count = 0

      payload = {'id': 1, 'value': count, 'wsid': wsid}
      self.send_message(payload)

      twitter_api = get_twitter_api(self.user_id)

      if twitter_api is None:
         return

      batch_limit = 100
      if self.max_tweets < 100:
         # única pesquisa
         batch_limit = self.max_tweets

         search_results = twitter_api.search.tweets(q=self.term, count=batch_limit)
         statuses = search_results['statuses']

         self.save_batch_tweets(statuses, wsid, len(statuses))
      else:
         # várias pesquisas até o limite estipulado
         max_results = min(MAX_TWEETS_FOR_FIND_OUT, self.max_tweets)

         # recuperando a primeira leva de tweets (de 200 em 200)
         search_results = twitter_api.search.tweets(q=self.term, count=200)
         statuses = search_results['statuses']

         self.save_batch_tweets(statuses, wsid, len(statuses))

         for _ in range(10):
            try:
               next_results = search_results['search_metadata']['next_results']
            except KeyError as e:
               raise

            kwargs = dict([ kv.split('=')
                         for kv in next_results[1:].split('&') ])

            search_results = twitter_api.search.tweets(**kwargs)

            round_tweets = search_results['statuses']
            statuses += round_tweets

            self.save_batch_tweets(round_tweets, wsid, len(statuses))

            if len(statuses) >= max_results:
               break

      return statuses

   def save_batch_tweets(self, batch_tweets, wsid, count):
      for tw in batch_tweets:
         self.save_tweet(tw)

      payload = {'id': 1, 'value': count, 'wsid': wsid}
      self.send_message(payload)

      das_tretas_vish(batch_tweets)
