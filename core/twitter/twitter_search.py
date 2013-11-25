#!/bin/python3.3.2
# -`*- coding: utf-8 -*-
from core.twitter.twitter_lookup import TwitterLookUp, MAX_TWEETS_FOR_FIND_OUT
from core.twitter.twitter_oauth_dance import get_twitter_api
from core.exceptions.crawl_exceptions import MaxTweetsReachError

from core.twitter.utils import das_tretas_vish

import simplejson as json
from core.data.orm.database import db_session
from core.data.orm.models import Analyze

class TwitterSearch(TwitterLookUp):
   def search(self, wsid):
      count = -1

      payload = {
         'id': 1,
         'value': count,
         'wsid': wsid,
         'anl_mcWords': 0,
         'anl_mcNames': 0,
         'anl_mcHashs': 0,
         'anl_lexDivWords': 0,
         'anl_avgWords': 0
      }

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

         self.save_batch_tweets(statuses)
         self.perform_analyzes(statuses, wsid)

         # notificando front para finalizar
         print("incompleto")
         self.finish_analyzes(wsid)
      else:
         # várias pesquisas até o limite estipulado
         max_results = min(MAX_TWEETS_FOR_FIND_OUT, self.max_tweets)

         # recuperando a primeira leva de tweets (de 200 em 200)
         search_results = twitter_api.search.tweets(q=self.term, count=200)
         statuses = search_results['statuses']

         self.save_batch_tweets(statuses)
         self.perform_analyzes(statuses, wsid)

         for _ in range(10):
            try:
               next_results = search_results['search_metadata']['next_results']
            except KeyError as e:
               # notificando front para finalizar
               self.finish_analyzes(wsid)
               break
               # print("treta")
               # raise

            kwargs = dict([ kv.split('=')
                         for kv in next_results[1:].split('&') ])

            search_results = twitter_api.search.tweets(**kwargs)

            round_tweets = search_results['statuses']
            statuses += round_tweets

            self.save_batch_tweets(round_tweets)
            self.perform_analyzes(statuses, wsid)

            if len(statuses) >= max_results:
               # notificando front para finalizar
               self.finish_analyzes(wsid)
               break

      return statuses

   def finish_analyzes(self, wsid):
      # notificando front para finalizar
      payload = {
         'id': 1,
         'value': 0,
         'wsid': wsid,
         'anl_mcWords': 0,
         'anl_mcNames': 0,
         'anl_mcHashs': 0,
         'anl_lexDivWords': 0,
         'anl_avgWords': 0
      }

      self.send_message(payload)

   def save_batch_tweets(self, batch_tweets):
      for tw in batch_tweets:
         self.save_tweet(tw)

   def perform_analyzes(self, tweets, wsid):

      count = len(tweets)

      mcWords, mcNames, mcHashs, lexDivWords, avgWords = das_tretas_vish(tweets)

      # words
      catWords = [ (k) for (k,v) in mcWords ]
      datWords = [ (v) for (k,v) in mcWords ]

      anl_mcWords = Analyze("mcWords", json.dumps(catWords), json.dumps(datWords), count, self.tfo_id)
      db_session.add(anl_mcWords)
      db_session.commit()

      # names
      catNames = [ (k) for (k,v) in mcNames ]
      datNames = [ (v) for (k,v) in mcNames ]

      anl_mcNames = Analyze("mcNames", json.dumps(catNames), json.dumps(datNames), count, self.tfo_id)
      db_session.add(anl_mcNames)
      db_session.commit()

      # hashtags
      catHashs = [ (k) for (k,v) in mcHashs ]
      datHashs = [ (v) for (k,v) in mcHashs ]

      anl_mcHashs = Analyze("mcHashs", json.dumps(catHashs), json.dumps(datHashs), count, self.tfo_id)
      db_session.add(anl_mcHashs)
      db_session.commit()

      # diversidade lexica
      anl_lexDivWords = Analyze("lexDivWords", None, json.dumps(lexDivWords), count, self.tfo_id)
      db_session.add(anl_lexDivWords)
      db_session.commit()

      # media de palavras
      anl_avgWords = Analyze("avgWords", None, json.dumps(avgWords), count, self.tfo_id)
      db_session.add(anl_avgWords)
      db_session.commit()

      # notificando front
      payload = {
         'id': 1,
         'value': count,
         'wsid': wsid,
         'anl_mcWords': anl_mcWords.id,
         'anl_mcNames': anl_mcNames.id,
         'anl_mcHashs': anl_mcHashs.id,
         'anl_lexDivWords': anl_lexDivWords.id,
         'anl_avgWords': anl_avgWords.id
      }

      self.send_message(payload)
