#!/bin/python3.3.2
# -`*- coding: utf-8 -*-
import os
from webapp import app
from flask import request, session, g, redirect, url_for, abort, render_template, flash, send_from_directory, jsonify

from core.twitter.twitter_oauth_dance import mrcrawler_oauth_dance
from core.data.orm.database import db_session
from core.data.orm.models import User

from core.twitter.twitter_stream import TwitterStream
from concurrent import futures

@app.teardown_appcontext
def shutdown_session(exception=None):
   db_session.remove()

@app.route('/favicon.ico')
def favicon():
   return send_from_directory(os.path.join(app.root_path, 'static'), 'ico/favicon.ico')

@app.errorhandler(404)
def page_not_found(e):
   return render_template('404.html'), 404

@app.route('/')
def index():
   return render_template('index.html')

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
   session.pop('user_name', None)
   session.pop('logged_in', None)
   return redirect(url_for('index'))

@app.route('/_twitter_lookup')
def add_numbers():
   term = request.args.get('term')
   wsid = request.args.get('wsid')
   # b = request.args.get('b', 0, type=int)

   user_id = session['user_id']

   ct = TwitterStream(term, "twitter_stream", 100, user_id)
   executor = futures.ProcessPoolExecutor(max_workers=1)


   #ct.listen(wsid)
   future = executor.submit(ct.listen, wsid)

   # print(future.result())

   return jsonify(result="Iniciado")
