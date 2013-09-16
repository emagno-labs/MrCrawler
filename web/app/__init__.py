from flask import Flask
from cherrypy import wsgiserver

# configuracao da aplicacao web
SECRET_KEY = 'devkey' # para a session
USERNAME = 'admin'
PASSWORD = 'default'

# criando a aplicacao web
app = Flask(__name__)
app.config.from_object(__name__)

# importando as views
import web.app.views

# preparando o servidor web (WSGI)
d = wsgiserver.WSGIPathInfoDispatcher({'/': app})
server = wsgiserver.CherryPyWSGIServer(('0.0.0.0', 8080), d)
