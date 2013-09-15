from flask import Flask, request, session, redirect, url_for, abort, render_template, flash, send_from_directory
from cherrypy import wsgiserver

# configuration
USERNAME = 'admin'
PASSWORD = 'default'

# criando a aplicacao
app = Flask(__name__)
app.config.from_object(__name__)

# web methods
@app.route('/busca', methods=['GET', 'POST'])
def busca():
   url = session['url']
   word = session['word']

   return render_template('busca.html', url='Teste')

@app.route('/')
def index():
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
         #session['logged_in'] = True
         return render_template('index.html', error=error)
         #flash('Você está autenticado :)')
         #return redirect(url_for('do_crawl'))
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

# o web server (WSGI)
d = wsgiserver.WSGIPathInfoDispatcher({'/': app})
server = wsgiserver.CherryPyWSGIServer(('0.0.0.0', 8080), d)

# iniciando a aplicacao
if __name__ == '__main__':
   try:
      server.start()
   except KeyboardInterrupt:
      server.stop()

