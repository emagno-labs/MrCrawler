from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from teste import app
import tornado.options

tornado.options.parse_command_line()

http_server = HTTPServer(WSGIContainer(app))
http_server.listen(5000)
try:
   IOLoop.instance().start()
except KeyboardInterrupt:
   IOLoop.instance().stop()
