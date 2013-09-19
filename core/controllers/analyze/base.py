import abc
from core.controllers.crawler.mrc import Crawl

class AbstractAnalyzer(object):
   __metaclass__ = abc.ABCMeta

   def __init__(self):
      pass

   @property
   def crawler(self): 
      return self._crawler

   @abc.abstractmethod
   def analyze(self):
      '''
      Este método realiza a análise de dados de uma determinada página retornada pelo crawler
      '''

      raise NotImplementedError("Módulo não está implementando o método requerido 'analize'")

   @abc.abstractmethod
   def storeData(self):
      '''
      Este método destina-se a registrar os dados analisados
      '''

      raise NotImplementedError("Módulo não está implementando o método requerido 'storeData'")
