#!/bin/python3.3.2
# -`*- coding: utf-8 -*-

from twitter import *
import simplejson as json
import time
from datetime import datetime
from bs4 import BeautifulSoup
from core.data.orm.database import db_session
from core.data.orm.models import Tweet
from core.exceptions.crawl_exceptions import MaxTweetsReachError
import requests

CONSUMER_KEY="Fim30iOMcDXiGWc59VjxhQ" 
CONSUMER_SECRET="GpYTUAeDhKqMhiFQwImVzdSZjw24kJR3QnmeRg6ME" 
 
OAUTH_TOKEN="22927044-HUBj3785kPqtA78Z04sdZb44BTWeY8rLG9ctDYGcA" 
OAUTH_SECRET="IvHBolYe5cehTl3sfSBaXvREtugUhz3n1TILjmKcc"

# quantidade máxima de tweets coletados. 0 = infinitos (ou até interrupção do usuário)
MAX_SEARCH = 0

class CrawlTwitter:
   def set_date(self, date_str):
      time_struct = time.strptime(date_str, "%a %b %d %H:%M:%S +0000 %Y")#Tue Apr 26 08:57:55 +0000 2011
      return datetime.fromtimestamp(time.mktime(time_struct))

   def get_text(self, markup):
      #try:
         soup = BeautifulSoup(markup, "lxml")
         return soup.get_text()
      #except:
      #   return markup

   def save(self, tweet, filter_term):
      user = tweet.get('user')
   
      # persistindo em base de dados
      tw = Tweet()

      tw.text = tweet.get('text')
      tw.created_at = self.set_date(tweet.get('created_at'))
      tw.source = self.get_text(tweet.get('source'))

      # dados de geolocalizacao (se houver)

      geo = tweet.get('geo')
      if geo:
         # {'type': 'Point', 'coordinates': [36.0447981, 136.2608959]}
         coords = geo.get('coordinates')
         if coords:
            tw.lat = coords[0]
            tw.lng = coords[1]  

      tw.term = filter_term
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

   def listen(self, filter_term, max_tweets, wsid):
      print ("Iniciando captura dos dados")

      twitter_stream = TwitterStream(auth=OAuth(OAUTH_TOKEN, OAUTH_SECRET, CONSUMER_KEY, CONSUMER_SECRET))
      iterator = twitter_stream.statuses.filter(track=filter_term)

      count = 0

      try:
         payload = {'id': 1, 'value': 1000, 'wsid': wsid}
         r = requests.get("http://localhost:8080/api", params=payload, timeout=0.001)
         print (r.url)
         print (r.status_code)
      except:
         pass


      try:
         for tweet in iterator:
            #print(tweet)

            #json.dump(tweet, f, indent=3)

            if tweet.get('text'):
               if tweet.get('geo'):
                  print ("Geo: %s" % tweet.get('geo'))
               else:
                  print ("Sem geolocalizacao")

               print ("Mensagem: %s" % tweet.get('text'))
               print ("Data: %s" % tweet.get('created_at'))
               print ("Origem: %s" % tweet.get('source'))
   
               user = tweet.get('user')
   
               print ("Nome: %s [%d]" % (user.get('name'), user.get('id')))
               print ("%s" % user.get('description'))
               print ("Criado em: %s" % user.get('created_at'))
               print ("Seguidores [%s], Seguindo [%s], Amigos [%s]" % (user.get('followers_count'), user.get('following'), user.get('friends_count')))
               print ("Geo Habilitado: %s" % user.get('geo_enabled'))
               print ("Url: %s" % user.get('url'))
               print ("Url Imagem: %s" % user.get('profile_image_url'))
               print ("========================")
               print (" ")

               self.save(tweet, filter_term)
               count = count + 1

               try:
                  payload = {'id': 1, 'value': count, 'wsid': wsid}
                  r = requests.get("http://localhost:8080/api", params=payload, timeout=0.001)
                  print (r.url)
                  print (r.status_code)
               except:
                  pass

               if count == max_tweets and max_tweets > 0:
                  err = "Foi alcançado o máximo de tweets para serem capturados: [%d]"
                  raise MaxTweetsReachError(err % max_tweets)
      
      except MaxTweetsReachError as e:
         print ("Leitura interrompida. Motivo: %s" % e.value)
      except KeyboardInterrupt:
         print ("Leitura interrompida. Motivo: Forçado pelo usuário")

