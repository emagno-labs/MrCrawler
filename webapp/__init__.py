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
from tornado.websocket import WebSocketHandler
from tornado.web import Application, FallbackHandler, RequestHandler
from tornado import web
import json
import uuid
from core.crawler.crawl_twitter import CrawlTwitter
import requests

# configuracao da aplicacao Flask. TODO externalizar em um arquivo próprio
SECRET_KEY = 'devkey' # para a session
USERNAME = 'admin'
PASSWORD = 'default'

# criando a aplicacao web
app = Flask(__name__)
app.config.from_object(__name__)

# importando as views
import webapp.views

# preparando o servidor web (WSGI)

clientes = [] # de clientes do websocket

class SocketHandler(WebSocketHandler):
   def open(self):
      if self not in clientes:
         self.id = uuid.uuid4()
         clientes.append(self)

   def on_message(self, message):
      '''
      json.load para carregar a mensagem
      pode ser: init_listener
      ou: finish_listener
      '''
      if message == "init":
         data = {"wsid": str(self.id)}
         data = json.dumps(data)
         self.write_message(data)
         print ("wsid: %s" % str(self.id))
         
         from concurrent import futures
         executor = futures.ProcessPoolExecutor(max_workers=1)
         ct = CrawlTwitter()
         future = executor.submit(ct.listen, "#meta", 10, str(self.id))

         #try:
         #   payload = {'id': 1, 'value': 1000, 'wsid': str(self.id)}
         #   r = requests.get("http://localhost:8080/api", params=payload, timeout=0.001)
         #   print (r.url)
         #   print (r.status_code)
         #except:
         #   pass

         print ("Dados capturados")

   def on_close(self):
      if self in clientes:
         clientes.remove(self)

class ApiHandler(RequestHandler):

   @web.asynchronous
   def get(self, *args):
      self.finish()
      wsid = self.get_argument("wsid")
      id = self.get_argument("id")
      value = self.get_argument("value")
      data = {"id": id, "value" : value}
      data = json.dumps(data)

      for c in clientes:
         if str(c.id) == wsid:
            c.write_message(data)
   
   @web.asynchronous
   def post(self):
      pass

# habilitando linha de comando (utilizada para efetuar o logging no console: --logging=debug)
tornado.options.parse_command_line() 

# inicializando o http server e configurando a porta 
#http_server = HTTPServer(WSGIContainer(app))
#http_server.listen(8080)

wsgi_app = WSGIContainer(app)

application = Application([
   (r'/ws', SocketHandler),
   (r'/api', ApiHandler),
   (r'.*', FallbackHandler, dict(fallback=wsgi_app))
])

application.listen(8080)

# inicializando a instancia de IO
server = IOLoop.instance()
