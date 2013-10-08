#!/bin/python3.3.2
# -`*- coding: utf-8 -*-

"""
Este módulo representa a classe 'Page', responsável por armazenar os dados de uma página "crawleada"
"""

class Page(object):

   def __init__(self):
      self.soup = None
      self.markup = None
      self.text = None
      self.links = []
      self.scripts = []
      self.comments = []
