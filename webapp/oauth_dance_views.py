#!/bin/python3.3.2
# -`*- coding: utf-8 -*-
from webapp import app
from flask import request, redirect, url_for, render_template, session
from datetime import datetime

from core.twitter.twitter_oauth_dance import get_user_oauth_tokens, get_user_credentials

from core.data.orm.models import User
from core.data.orm.database import db_session

@app.route("/oauth_helper")
def oauth_helper():
   '''
   Este método é responsável por capturar o retorno (callback) do Twitter
   '''
   is_denied, oauth_token, oauth_verifier = is_oauth_denied(request)

   if is_denied:
      remove_user_by_public_token(oauth_token)
   else:
      try:
         update_user_tokens(oauth_token, oauth_verifier)
      except:
         remove_user_by_public_token(oauth_token)

   return render_template('index.html')

def is_oauth_denied(req):
   denied_oauth_token = request.args.get('denied')

   if denied_oauth_token is not None:
      return True, denied_oauth_token, None
   else:
      oauth_token = request.args.get('oauth_token')
      oauth_verifier = request.args.get('oauth_verifier')

      return False, oauth_token, oauth_verifier

def remove_user_by_public_token(oauth_token):
   user = User.query.filter(User.oauth_token == oauth_token).first()

   if user is not None:
      db_session.delete(user)
      db_session.commit()

   session.pop('user_id', None)
   session.pop('user_name', None)
   session.pop('logged_in', None)

def update_user_tokens(oauth_token, oauth_verifier):
   '''
   Este método recupera as credenciais definitivas do usuário + informações do Twitter
   '''
   # recupera a sessao a partir do token publico (temporario)
   temp_user = User.query.filter(User.oauth_token == oauth_token).first()

   if temp_user is None:
      print ("Não foi possível recuperar usuário para token temporário [%s]. Prosseguindo com sessão atual." % oauth_token)
      return

   oauth_token_secret = temp_user.oauth_token_secret

   # a partir dos tokens temporarios + o verificador, recupera os tokens permanentes
   oauth_token, oauth_token_secret = get_user_oauth_tokens(oauth_token, oauth_token_secret, oauth_verifier)

   # verifica se o token privado já existe na base (usuário já se logou um dia)
   user = User.query.filter(User.oauth_token_secret == oauth_token_secret).first()

   if user is None:
      # primeiro acesso, atualiza o usuário temporário para ser o definitivo
      user = temp_user
   else:
      # já acessou um dia exclui a temporaria
      db_session.delete(temp_user)

   # atualizando as credenciais definitivas do usuário
   user.oauth_token = oauth_token
   user.oauth_token_secret = oauth_token_secret
   user.last_access = datetime.now()
   user.is_temporary = False

   # recuperando dados do usuário no twitter
   credentials = get_user_credentials(oauth_token, oauth_token_secret)

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

   session['user_id'] = user.id
   session['user_name'] = user.name
   session['logged_in'] = True
