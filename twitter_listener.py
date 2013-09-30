from twitter import *
import simplejson as json
import time
from datetime import datetime
from bs4 import BeautifulSoup
from core.data.orm.database import db_session
from core.data.orm.models import Tweet

CONSUMER_KEY="Fim30iOMcDXiGWc59VjxhQ" 
CONSUMER_SECRET="GpYTUAeDhKqMhiFQwImVzdSZjw24kJR3QnmeRg6ME" 
 
OAUTH_TOKEN="22927044-HUBj3785kPqtA78Z04sdZb44BTWeY8rLG9ctDYGcA" 
OAUTH_SECRET="IvHBolYe5cehTl3sfSBaXvREtugUhz3n1TILjmKcc"

#f = open('basic-pretty.json', mode='w', encoding='utf-8')

def set_date(date_str):
   time_struct = time.strptime(date_str, "%a %b %d %H:%M:%S +0000 %Y")#Tue Apr 26 08:57:55 +0000 2011
   return datetime.fromtimestamp(time.mktime(time_struct))

def get_text(markup):
   soup = BeautifulSoup(markup, "lxml")
   return soup.get_text()

twitter_stream = TwitterStream(auth=OAuth(OAUTH_TOKEN, OAUTH_SECRET, CONSUMER_KEY, CONSUMER_SECRET))
iterator = twitter_stream.statuses.filter(track='cruzeiro')

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
      
         # persistindo em base de dados
         tw = Tweet()
         tw.text = tweet.get('text')
         tw.created_at = set_date(tweet.get('created_at'))
         tw.source = get_text(tweet.get('source'))
         tw.user_name = user.get('name')
         tw.user_id = user.get('id')
         tw.user_description = user.get('description')
         tw.user_created_at = set_date(user.get('created_at'))
         tw.user_followers_count = user.get('followers_count')
         tw.user_friends_count = user.get('friends_count')
         tw.user_profile_image_url = user.get('profile_image_url')
         tw.tweet = json.dumps(tweet)

         db_session.add(tw)
         db_session.commit()
except KeyboardInterrupt:
   print ("Leitura interrompida pelo usuário")

