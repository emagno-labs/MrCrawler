'''
Este módulo é responsável por realizar a coleta das informações (crawl) de um site.
Os dados coletados serão armazenados para que seja realizadas análises e auditorias.

moduleauthor:: Eryckson Magno <eryckson@me.com>
'''

from urllib import parse
from urllib.request import urlopen
from bs4 import BeautifulSoup, Comment
from core.exceptions.crawl_exceptions import *

class Crawl(object):

   def __init__(self, url):
      self._url = url
      self._soup = None

   def makeTheSoup(self):
      '''
      Este método "le" uma url e a transforma no objeto "parseado" pelo  bs4
      '''

      if self._url is None:
         raise InvalidArgumentError('Dados insuficientes para efetuar a coleta de informações.', ('url'))

      try:
         # abrindo a url e obtendo a resposta 
         response = urlopen(self._url)

         # fazendo a "sopa" do retorno utilizando o lxml como parser
         self._soup = BeautifulSoup(response.read(), "lxml")
      except:
         raise MakeTheSoupError(self._url, "lxml")

   def getMarkup(self):
      '''
      Este método retorna o HTML (markup) da página.
      
      :param soup: o objeto bs4 com a página "parseada"
      :return: text -- o markup, ou "None" caso não houver
      '''
      
      try:
         return self._soup.prettify()
      except:
         raise

   def getText(self):
      '''
      Este método retorna todo (e somente) o texto da página (útil para pesquisa de conteúdo, estimativa de ocorrência de palavras, etc)
      
      :param soup: o objeto bs4 com a página "parseada"
      :return: text -- todo o texto
      '''
      
      try:
         return self._soup.get_text()
      except:
         raise

   def getLinks(self):
      '''
      Este método localiza e separa todos os links de uma página.

      :return: uma lista com os links recuperados
      '''
      
      try:
         links = []

         for l in self._soup.find_all('a'):
            value = l.get('href')
            newUrl = parse.urljoin(self._url, value)
            links = links + [newUrl]

         return links
      except:
         raise

   def getScripts(self):
      '''
      Este método localiza e retorna os scripts da página.
      
      :return: uma lista com os scripts localizados
      '''
      
      try:
         return self._soup.find_all('script')
      except:
         raise

   def getComments(self):
      '''
      Este método localiza todos os comentários do código.

      :return: uma lista com os comentários
      '''

      try:
         comments = self._soup.find_all(text=lambda text:isinstance(text, Comment))
         return comments
      except:
         raise
