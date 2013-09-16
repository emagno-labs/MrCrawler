'''
Este módulo é responsável por:
   1) criar uma aplicação Flask (routing + templating)
   2) criar um servidor tornado (wsgi server)
'''

from flask import Flask
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
import tornado.options

# configuracao da aplicacao Flask. TODO externalizar em um arquivo próprio
SECRET_KEY = 'devkey' # para a session
USERNAME = 'admin'
PASSWORD = 'default'

# criando a aplicacao web
app = Flask(__name__)
app.config.from_object(__name__)

# importando as views
import web.app.views

# preparando o servidor web (WSGI)

# habilitando linha de comando (utilizada para efetuar o logging no console: --logging=debug)
tornado.options.parse_command_line() 

# inicializando o http server e configurando a porta 
http_server = HTTPServer(WSGIContainer(app))
http_server.listen(8080)

# inicializando a instancia de IO
server = IOLoop.instance()
