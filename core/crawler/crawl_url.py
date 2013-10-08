#!/bin/python3.3.2
# -`*- coding: utf-8 -*-

'''
Este módulo é responsável por realizar a coleta das informações (crawl) de um site.
Os dados coletados serão armazenados para que seja realizadas análises e auditorias.
'''

from urllib import parse
from urllib.request import urlopen
from bs4 import BeautifulSoup, Comment
from core.exceptions.crawl_exceptions import *
from core.controllers.crawler.page import Page

class CrawlUrl(object):

   def __init__(self, url):
      self._url = url

   def makeTheSoup(self):
      '''
      Este método dispara diversos métodos privados para devolver um objeto "Page" com os dados de uma url "crawleados"
      '''
      
      try:
         if self._url is None:
            raise InvalidArgumentError('Dados insuficientes para efetuar a coleta de informações.', ('url'))
         
         page = Page()

         page.soup = self.getSoup()
         page.markup = self.getMarkup(page.soup)
         page.text = self.getText(page.soup)
         page.links = self.getLinks(page.soup)
         page.scripts = self.getScripts(page.soup)
         page.comments = self.getComments(page.soup)

         return page
      except KeyboardInterrupt:
         raise
      except:
         raise MakeTheSoupError(self._url, "lxml")

   def getSoup(self):
      '''
      Este método "le" uma url e a transforma no objeto "parseado" pelo  bs4
      '''

      try:
         # abrindo a url e obtendo a resposta 
         response = urlopen(self._url)

         # fazendo a "sopa" do retorno utilizando o lxml como parser
         soup = BeautifulSoup(response.read(), "lxml")

         return soup
      except:
         raise

   def getMarkup(self, soup):
      '''
      Este método retorna o HTML (markup) da página.
      
      :param soup: o objeto bs4 com a página "parseada"
      :return: text -- o markup, ou "None" caso não houver
      '''
      
      try:
         return soup.prettify()
      except:
         raise

   def getText(self, soup):
      '''
      Este método retorna todo (e somente) o texto da página (útil para pesquisa de conteúdo, estimativa de ocorrência de palavras, etc)
      
      :param soup: o objeto bs4 com a página "parseada"
      :return: text -- todo o texto
      '''
      try:
         return soup.get_text()
      except:
         raise

   def getLinks(self, soup):
      '''
      Este método localiza e separa todos os links de uma página.

      :return: uma lista com os links recuperados
      '''
      
      try:
         links = []

         for l in soup.find_all('a'):
            value = l.get('href')
            newUrl = parse.urljoin(self._url, value)
            links = links + [newUrl]

         return links
      except:
         raise

   def getScripts(self, soup):
      '''
      Este método localiza e retorna os scripts da página.
      
      :return: uma lista com os scripts localizados
      '''
      
      try:
         return soup.find_all('script')
      except:
         raise

   def getComments(self, soup):
      '''
      Este método localiza todos os comentários do código.

      :return: uma lista com os comentários
      '''

      try:
         comments = soup.find_all(text=lambda text:isinstance(text, Comment))
         return comments
      except:
         raise
