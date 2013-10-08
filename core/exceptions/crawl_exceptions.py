#!/bin/python3.3.2 
# -`*- coding: utf-8 -*-

'''
Este módulo define a estrutura de exceções para o pacote core.controllers.crawler
'''

from core.exceptions.base_exceptions import MrCrawlerError

class CrawlError(MrCrawlerError):
   pass

class InvalidArgumentError(CrawlError):
   '''
   Exceção disparada por erro de parametros inválidos/não informados
   '''

   def __init__(self, value, params=()):
      CrawlError.__init__(self, value)
      self.params = params

   def __str__(self):
      value = self.value

      if self.params:
         value += "\nOs seguintes parametros são inválidos:"

         for p in self.params:
            value += "\n-> %s" % p

      return value

   __repr__ = __str__

class MakeTheSoupError(CrawlError):
   '''
   Exceção disparada por erro no momento de "parsear" uma url no "crawl"
   '''
   
   def __init__(self, urlError, parser):
      CrawlError.__init__(self, urlError)
      self.parser = parser

   def __str__(self):
      error = "Erro ao realizar o parse via bs4 da url '%s' utilizando o parser '%s'."
      return (error % (self.value, self.parser))

   __repr__ = __str__

class CrawlTwitterError(CrawlError):
   pass

class MaxTweetsReachError(CrawlTwitterError):
   '''
   Exceção disparada quando é alcançado o limite de tweets para captura
   '''

   def __init__(self, value):
      CrawlTwitterError.__init__(self, value)

   def __str__(self):
      return self.value

   __repr__ = __str__
