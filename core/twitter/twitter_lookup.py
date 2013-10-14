#!/bin/python3.3.2
# -`*- coding: utf-8 -*-
import time
from datetime import datetime
from bs4 import BeautifulSoup
import simplejson as json
import requests

from core.data.orm.database import db_session
from core.data.orm.models import Tweet, TweetFindOut

MAX_TWEETS_FOR_FIND_OUT = 1500

class TwitterLookUp:

   tfo_id = None
   term = None
   search_type = None
   max_tweets = 0
   user_id = None

   def __init__(self, term, search_type, user_id, max_tweets=MAX_TWEETS_FOR_FIND_OUT):
      tfo = TweetFindOut(term, search_type, max_tweets, user_id)
      db_session.add(tfo)
      db_session.commit()

      self.tfo_id = tfo.id
      self.term = term
      self.search_type = search_type
      self.max_tweets = max_tweets
      self.user_id = user_id

   def send_message(self, message_payload):
      try:
         # payload = {'id': 1, 'value': count, 'wsid': wsid}
         r = requests.get("http://localhost:8080/api", params=message_payload, timeout=0.001)
      except:
         pass

   def set_date(self, date_str):
      time_struct = time.strptime(date_str, "%a %b %d %H:%M:%S +0000 %Y")#Tue Apr 26 08:57:55 +0000 2011
      return datetime.fromtimestamp(time.mktime(time_struct))

   def get_text(self, markup):
      try:
         soup = BeautifulSoup(markup, "lxml")
         return soup.get_text()
      except:
         return markup

   def print_tweet(self, tweet):
      print ("Latitude: %s | Longitute: %s" % (tweet.lat, tweet.lng))
      print ("Mensagem: %s" % tweet.text)
      print ("Data: %s" % tweet.created_at.strftime("%d/%m/%Y %H:%M"))
      print ("Origem: %s" % tweet.source)
      print ("Nome: %s [%d]" % (tweet.user_name, tweet.user_id))
      print ("%s" % tweet.user_description)
      print ("Criado em: %s" % tweet.user_created_at.strftime("%d/%m/%Y %H:%M"))
      print ("Seguidores [%d], Amigos [%d]" % (tweet.user_followers_count, tweet.user_friends_count))
      print ("Url Imagem: %s" % tweet.user_profile_image_url)
      print ("--------------------------------------------------------")

   def get_geodata(self, geo):
      # {'type': 'Point', 'coordinates': [36.0447981, 136.2608959]}
      if geo:
         coords = geo.get('coordinates')
         if coords:
            return coords[0], coords[1]
      return None, None

   def save_tweet(self, tweet):
      # persistindo em base de dados
      tw = Tweet()

      # relacionando com a busca realizada
      tw.tweet_find_out_id = self.tfo_id

      tw.text = tweet.get('text')
      tw.created_at = self.set_date(tweet.get('created_at'))
      tw.source = self.get_text(tweet.get('source'))
      tw.lat, tw.lng = self.get_geodata(tweet.get('geo'))

      user = tweet.get('user')

      tw.user_name = user.get('name')
      tw.user_id = user.get('id')
      tw.user_description = user.get('description')
      tw.user_created_at = self.set_date(user.get('created_at'))
      tw.user_followers_count = user.get('followers_count')
      tw.user_friends_count = user.get('friends_count')
      tw.user_profile_image_url = user.get('profile_image_url')

      # salvando o json original
      tw.tweet = json.dumps(tweet)

      db_session.add(tw)
      db_session.commit()

      self.print_tweet(tw)
