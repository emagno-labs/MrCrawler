from core.web import app
from flask import request, session, g, redirect, url_for, abort, render_template, flash, send_from_directory
import os

# web methods
@app.route('/busca', methods=['GET', 'POST'])
def busca():
   url = session['url']
   word = session['word']

   return render_template('busca.html', url='Teste')

@app.route('/')
def index():
   session['teste'] = 'teste'
   return render_template('index.html')

@app.route('/do_crawl', methods=['GET', 'POST'])
def do_crawl():
   error = None
   if request.method == 'POST':
      url = request.form['url']
      word = request.form['word']
      if not url:
         error = 'A url deve ser informada!'
      elif not word:
         error = 'A palavra deve ser informada!'
      else:
         session['url'] = url
         session['word'] = word
         flash('Busca sendo realizada!')
         return redirect(url_for('busca'))
   return render_template('index.html', error=error)

@app.route('/login', methods=['GET', 'POST'])
def login():
   error = None
   if request.method == 'POST':
      if request.form['username'] != app.config['USERNAME']:
         error = 'Credenciais inválidas'
      elif request.form['password'] != app.config['PASSWORD']:
         error = 'Credenciais inválidas'
      else:
         session['logged_in'] = True
         flash('Você está autenticado :)')
         return redirect(url_for('do_crawl'))
   return render_template('login.html', error=error)

@app.route('/logout')
def logout():
   session.pop('logged_in', None)
   flash('Você saiu :(')
   return redirect(url_for('index'))

@app.route('/favicon.ico')
def favicon():
   return send_from_directory(os.path.join(app.root_path, 'static'), 'ico/favicon.ico')

@app.errorhandler(404)
def page_not_found(e):
   return render_template('404.html'), 404
