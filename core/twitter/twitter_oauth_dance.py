#!/bin/python3.3.2
# -`*- coding: utf-8 -*-
import twitter
from twitter.oauth_dance import parse_oauth_tokens
from flask import request, url_for

from core.data.orm.models import User
from core.data.orm.database import db_session

CONSUMER_KEY = 'Fim30iOMcDXiGWc59VjxhQ'
CONSUMER_SECRET = 'GpYTUAeDhKqMhiFQwImVzdSZjw24kJR3QnmeRg6ME'

TWITTER_URL_AUTHORIZE = 'http://api.twitter.com/oauth/authorize?oauth_token='

def mrcrawler_oauth_dance():
   '''
   Este método abre uma aba solicitando que o usuário autorize o Mr. Crawler
   a acessar sua conta do twitter (login)
   '''
   browser = request.user_agent.browser
   host = request.host

   _twitter_oauth = twitter.OAuth('', '', CONSUMER_KEY, CONSUMER_SECRET)
   _twitter = twitter.Twitter(auth=_twitter_oauth, format='', api_version=None)

   oauth_callback = "http://" + host + url_for('oauth_helper')

   oauth_token, oauth_token_secret = parse_oauth_tokens(
      _twitter.oauth.request_token(oauth_callback=oauth_callback))

   # criando um usuário temporário
   user = User(oauth_token, oauth_token_secret, None, browser)
   db_session.add(user)
   db_session.commit()

   return (TWITTER_URL_AUTHORIZE + oauth_token)

def get_user_oauth_tokens(oauth_token, oauth_token_secret, oauth_verifier):
   '''
   a partir dos tokens temporarios + o verificador, recupera os tokens permanentes
   '''
   _twitter_oauth = twitter.OAuth(oauth_token, oauth_token_secret, CONSUMER_KEY, CONSUMER_SECRET)
   _twitter = twitter.Twitter(auth=_twitter_oauth, format='', api_version=None)

   return parse_oauth_tokens(_twitter.oauth.access_token(oauth_verifier=oauth_verifier))

def get_user_credentials(oauth_token, oauth_token_secret):
   '''
   recupera os dados da conta do usuário no twitter
   '''
   _twitter_oauth = twitter.OAuth(oauth_token, oauth_token_secret, CONSUMER_KEY, CONSUMER_SECRET)
   _twitter = twitter.Twitter(auth=_twitter_oauth, api_version='1.1', domain='api.twitter.com')

   return _twitter.account.verify_credentials()

def get_twitter_stream(user_id):
   '''
   Obtendo twitter_stream para usuario
   '''
   user = User.query.filter(User.id == user_id).first()

   if user is not None:
      _twitter_oauth = twitter.OAuth(user.oauth_token, user.oauth_token_secret, CONSUMER_KEY, CONSUMER_SECRET)
      twitter_stream = twitter.TwitterStream(auth=_twitter_oauth)

      return twitter_stream
   else:
      return None

def get_twitter_search(user_id):
   '''
   Obtendo twitter "search" para usuário
   '''
   pass
