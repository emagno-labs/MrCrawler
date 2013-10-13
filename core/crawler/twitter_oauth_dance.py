#!/bin/python3.3.2
# -`*- coding: utf-8 -*-

import twitter
from twitter.oauth_dance import parse_oauth_tokens

from core.data.orm.models import User
from core.data.orm.database import db_session

import webbrowser
from datetime import datetime
from webapp import app
from flask import request, redirect, url_for, render_template, session

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

def remove_user_by_public_token(oauth_token):
   # recupera o usuário temporário para remoção
   print("Removendo [%s]" % oauth_token)

   temp_user = User.query.filter(User.oauth_token == oauth_token).first()

   if temp_user is not None:
      db_session.delete(temp_user)
      db_session.commit()

   session.pop('user_id', None)
   session.pop('user_name', None)
   session.pop('logged_in', None)
   return render_template('index.html')

@app.route("/oauth_helper")
def oauth_helper():
   '''
   Este método é responsável por capturar o retorno (callback) vindo do
   site do Twitter após a solicitação de autorização (login) do usuário
   '''
   try:
      oauth_token = request.args.get('denied')

      if oauth_token is not None:
         return remove_user_by_public_token(oauth_token)
   except:
      # caso não seja devolvido o retorno de negação, então vai gerar uma exceção
      pass

   try:
      oauth_verifier = request.args.get('oauth_verifier')
      oauth_token = request.args.get('oauth_token')

      oauth_token_to_remove = oauth_token

      browser = request.user_agent.browser

      # recupera a sessao a partir do token publico (temporario)
      temp_user = User.query.filter(User.oauth_token == oauth_token).first()

      # recupera o token secreto (temporario)
      oauth_token_secret = temp_user.oauth_token_secret

      # a partir dos tokens temporarios + o verificador, recupera os tokens permanentes
      _twitter_oauth = twitter.OAuth(oauth_token, oauth_token_secret, CONSUMER_KEY, CONSUMER_SECRET)
      _twitter = twitter.Twitter(auth=_twitter_oauth, format='', api_version=None)

      oauth_token, oauth_token_secret = parse_oauth_tokens(
         _twitter.oauth.access_token(oauth_verifier=oauth_verifier))

      # verifica se o token privado já existe na base (usuário já se logou um dia)
      user = User.query.filter(User.oauth_token_secret == oauth_token_secret).first()

      if user is None:
         # primeiro acesso, atualiza o usuário temporário para ser o definitivo
         user = temp_user

      else:
         # já acessou um dia exclui a temporaria
         db_session.delete(temp_user)

      user.oauth_token = oauth_token
      user.oauth_token_secret = oauth_token_secret
      user.last_access = datetime.now()
      user.browser = browser
      user.is_temporary = False

      # recuperando dados do usuário no twitter
      _twitter_oauth = twitter.OAuth(oauth_token, oauth_token_secret, CONSUMER_KEY, CONSUMER_SECRET)
      _twitter = twitter.Twitter(auth=_twitter_oauth, api_version='1.1', domain='api.twitter.com')

      credentials = _twitter.account.verify_credentials()

      user.id_twitter = credentials['id']
      user.name = credentials['name']
      user.screen_name = credentials['screen_name']
      user.description = credentials['description']
      user.lang = credentials['lang']
      user.time_zone = credentials['time_zone']
      user.location = credentials['location']
      user.geo_enabled = credentials['geo_enabled']
      user.url = credentials['url']
      user.profile_image_url = credentials['profile_image_url']
      user.friends_count = credentials['friends_count']
      user.statuses_count = credentials['statuses_count']
      user.favourites_count = credentials['favourites_count']

      db_session.commit()

      oauth_token_to_remove = oauth_token

      session['user_id'] = user.id
      session['user_name'] = user.name
      session['logged_in'] = True

      return render_template('index.html')
   except:
      # caso não seja devolvido retorno válido, ou em caso de exceção, removeremos o usuário temporário
      return remove_user_by_public_token(oauth_token_to_remove)
