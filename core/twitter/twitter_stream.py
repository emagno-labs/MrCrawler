#!/bin/python3.3.2
# -`*- coding: utf-8 -*-
from core.twitter.twitter_lookup import TwitterLookUp
from core.twitter.twitter_oauth_dance import get_twitter_stream
from core.exceptions.crawl_exceptions import MaxTweetsReachError

class TwitterStream(TwitterLookUp):
   def listen(self, filter_term, max_tweets, wsid, user_id):
      twitter_stream = get_twitter_stream(user_id)
      iterator = twitter_stream.statuses.filter(track=filter_term)

      count = 0

      payload = {'id': 1, 'value': count, 'wsid': wsid}
      self.send_message(payload)

      try:
         for tweet in iterator:
            self.save_tweet(tweet, filter_term)
            count = count + 1

            payload = {'id': 1, 'value': count, 'wsid': wsid}
            self.send_message(payload)

            if count == max_tweets and max_tweets > 0:
               err = "Foi alcançado o máximo de tweets para serem capturados: [%d]"
               raise MaxTweetsReachError(err % max_tweets)

      except MaxTweetsReachError as e:
         print ("Leitura interrompida. Motivo: %s" % e.value)
      except KeyboardInterrupt:
         print ("Leitura interrompida. Motivo: Forçado pelo usuário")
      except:
         raise
