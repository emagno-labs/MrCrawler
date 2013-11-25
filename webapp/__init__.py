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

from core.data.orm.models import Analyze
from core.data.orm.database import db_session

# configuracao da aplicacao Flask. TODO externalizar em um arquivo próprio
SECRET_KEY = 'devkey' # para a session
USERNAME = 'admin'
PASSWORD = 'default'

# criando a aplicacao web
app = Flask(__name__)
app.config.from_object(__name__)

# importando as views
import webapp.views
import webapp.oauth_dance_views

clientes = [] # de clientes do websocket

class SocketHandler(WebSocketHandler):
   '''
   Esta classe handler é responsável por iniciar uma comunicação via
   websockets entre o servidor e o cliente (browser)
   '''
   def open(self):
      if self not in clientes:
         self.id = uuid.uuid4()
         clientes.append(self)

         data = {"wsid": str(self.id)}
         data = json.dumps(data)
         self.write_message(data)

   def on_message(self, message):
      pass
      # if message is not None:
      # print ("wsid %s" % str(self.id))

      # data = {"wsid": str(self.id)}
      # data = json.dumps(data)
      # self.write_message(data)

      #    print ("wsid %s" % str(self.id))
      #    print ("Capturando tweets para o termo: %s " % message)

      #    # from concurrent import futures
      #    # executor = futures.ProcessPoolExecutor(max_workers=20)
      #    ct = TwitterStream()
      #    ct.listen(message, 100, str(self.id), 1)
      #    # future = executor.submit(ct.listen, message, 100, str(self.id), 1)

      #    print ("Tweets capturados")

   def on_close(self):
      if self in clientes:
         clientes.remove(self)

class ApiHandler(RequestHandler):
   '''
   Esta classe handler é responsável por receber uma notificação via api RESTful
   e enviar uma mensagem pelo websocket para os browsers clientes
   '''
   @web.asynchronous
   def get(self, *args):
      self.finish()

      wsid = self.get_argument("wsid")
      id = self.get_argument("id")
      value = self.get_argument("value")

      print(value)

      if value == "-1":
         data = {
            "id": id,
            "value" : -1,
            "catWords": 0,
            "datWords": 0,
            "catNames": 0,
            "datNames": 0,
            "catHashs": 0,
            "datHashs": 0,
            "lexDivWords": 0,
            "avgWords": 0
         }
      elif value == "0":
         data = {
            "id": id,
            "value" : 0,
            "catWords": 0,
            "datWords": 0,
            "catNames": 0,
            "datNames": 0,
            "catHashs": 0,
            "datHashs": 0,
            "lexDivWords": 0,
            "avgWords": 0
         }
      else:
         mcWordsId = self.get_argument("anl_mcWords")
         mcNamesId = self.get_argument("anl_mcNames")
         mcHashsId = self.get_argument("anl_mcHashs")
         lexDivWordsId = self.get_argument("anl_lexDivWords")
         avgWordsId = self.get_argument("anl_avgWords")

         anl_mcWords = Analyze.query.filter(Analyze.id == mcWordsId).first()
         anl_mcNames = Analyze.query.filter(Analyze.id == mcNamesId).first()
         anl_mcHashs = Analyze.query.filter(Analyze.id == mcHashsId).first()
         anl_lexDivWords = Analyze.query.filter(Analyze.id == lexDivWordsId).first()
         anl_avgWords = Analyze.query.filter(Analyze.id == avgWordsId).first()

         data = {
            "id": id,
            "value" : value,
            "catWords": anl_mcWords.label,
            "datWords": anl_mcWords.value,
            "catNames": anl_mcNames.label,
            "datNames": anl_mcNames.value,
            "catHashs": anl_mcHashs.label,
            "datHashs": anl_mcHashs.value,
            "lexDivWords": anl_lexDivWords.value,
            "avgWords": anl_avgWords.value
         }

      data = json.dumps(data)

      for c in clientes:
         if str(c.id) == wsid:
            c.write_message(data)

   @web.asynchronous
   def post(self):
      pass

# habilitando linha de comando (utilizada para efetuar o logging no console: --logging=debug)
tornado.options.parse_command_line()

wsgi_app = WSGIContainer(app)

application = Application([
   (r'/ws', SocketHandler),
   (r'/api', ApiHandler),
   (r'.*', FallbackHandler, dict(fallback=wsgi_app))
])

application.listen(8080)

# inicializando a instancia de IO
server = IOLoop.instance()
