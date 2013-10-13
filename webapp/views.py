#!/bin/python3.3.2
# -`*- coding: utf-8 -*-

from webapp import app
from flask import request, session, g, redirect, url_for, abort, render_template, flash, send_from_directory, jsonify
import os

from core.data.orm.database import db_session
from core.data.orm.models import User
from webapp.forms.auth import RegistrationForm

# imports para twitter (autenticação e coleta)
from core.crawler.twitter_oauth_dance import *

from core.crawler.crawl_twitter import CrawlTwitter
import twitter
from twitter.oauth_dance import parse_oauth_tokens
from twitter.oauth import read_token_file, write_token_file
import uuid
import webbrowser

@app.teardown_appcontext
def shutdown_session(exception=None):
   db_session.remove()

# web methods
@app.route('/busca', methods=['GET', 'POST'])
def busca():
   term = session['filter_term']

   return render_template('busca.html', filter_term=term)

@app.route('/_add_numbers')
def add_numbers():
   a = request.args.get('a', 0, type=int)
   b = request.args.get('b', 0, type=int)
   return jsonify(result=a + b)

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/do_crawl', methods=['GET', 'POST'])
def do_crawl():
   error = None
   if request.method == 'POST':
      term = request.form['filter_term']
      if not term:
         error = 'O termo da busca deve ser informado!'
      else:
         session['filter_term'] = term
         #flash('Busca sendo realizada!')
         #ct = CrawlTwitter()
         #ct.listen(term, 10)
         #return redirect(url_for('busca'))

         #data = {"id": 1, "value" : 100}
         #data = json.dumps(data)

         #for c in app.clientes:
         #   c.write_message(data)

   return render_template('index.html', error=error)

@app.route('/login')
def login():
   '''
   Este método redireciona para a página do twitter para que o usuário
   possa autorizar que o Mr. Crawler acesse sua conta
   '''
   return redirect(mrcrawler_oauth_dance())

@app.route('/logout')
def logout():
   session.pop('user_id', None)
   session.pop('logged_in', None)
   #flash('Você saiu :(')
   return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
   '''
   Este método obtém os dados do formulário e realiza o registro do usuário.
   '''
   form = RegistrationForm(request.form)

   if request.method == 'POST' and form.validate():
      user = User(form.login.data, form.name.data, form.email.data, form.password.data)
      db_session.add(user)
      db_session.commit()

      flash('Thanks for registering')
      session['logged_in'] = True
      return redirect(url_for('do_crawl'))

   return render_template('register.html', form=form)

@app.route('/favicon.ico')
def favicon():
   return send_from_directory(os.path.join(app.root_path, 'static'), 'ico/favicon.ico')

@app.errorhandler(404)
def page_not_found(e):
   return render_template('404.html'), 404
