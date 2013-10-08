#!/bin/python3.3.2
# -`*- coding: utf-8 -*-

'''
Este módulo define a estrutura de exceções para MrCrawler.
'''

class MrCrawlerError(Exception):
   '''
   Exceção base para o Mr Crawler.
   '''

   def __init__(self, value):
      Exception.__init__(self)
      self.value = str(value)

   def __str__(self):
      return self.value
