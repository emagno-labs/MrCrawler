#!/bin/python3.3.2
# -`*- coding: utf-8 -*-
from core.twitter.twitter_lookup import TwitterLookUp
from core.twitter.twitter_oauth_dance import get_twitter_stream
from core.exceptions.crawl_exceptions import MaxTweetsReachError

class TwitterStream(TwitterLookUp):
   def search(self, wsid):
      twitter_stream = get_twitter_stream(self.user_id)
      iterator = twitter_stream.statuses.filter(track=self.term)

      count = 0

      payload = {'id': 1, 'value': count, 'wsid': wsid}
      self.send_message(payload)

      try:
         for tweet in iterator:
            self.save_tweet(tweet)
            count = count + 1

            payload = {'id': 1, 'value': count, 'wsid': wsid}
            self.send_message(payload)

            # TODO limitar a pesquisa por tempo também
            if count == self.max_tweets and self.max_tweets > 0:
               err = "Foi alcançado o máximo de tweets para serem capturados: [%d]"
               raise MaxTweetsReachError(err % self.max_tweets)

      except MaxTweetsReachError as e:
         print ("Leitura interrompida. Motivo: %s" % e.value)
      except KeyboardInterrupt:
         print ("Leitura interrompida. Motivo: Forçado pelo usuário")
      except:
         raise
