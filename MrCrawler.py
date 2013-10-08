#!/bin/python3.3.2
# -`*- coding: utf-8 -*-

'''
Este módulo é responsável por iniciar o web server da aplicação web do Mr. Crawler
(pode ser considerado como o "main.py" do projeto)
'''

from webapp import server

if __name__ == '__main__':
   try:
      print ("Mr. Crawler iniciado e escutando em http://localhost:8080 ...")
      server.start()
   except KeyboardInterrupt:
      server.stop()
