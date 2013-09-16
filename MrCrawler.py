'''
Este módulo é responsável por iniciar o web server da aplicação web do Mr. Crawler
(pode ser considerado como o "main.py" do projeto)
'''

from web.app import server

if __name__ == '__main__':
   try:
      server.start()
   except KeyboardInterrupt:
      server.stop()
