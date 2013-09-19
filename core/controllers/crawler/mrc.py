'''
Este módulo é responsável por realizar o "spider" de uma url.
Ele irá, a partir da url inicial, listar todas as urls (links) desta e repetir o processo até atingir os limites estabelecidos.

moduleauthor:: Eryckson Magno <eryckson@me.com>
'''

from core.controllers.crawler.crawlurl import CrawlUrl 
from core.controllers.crawler.page import Page
from core.exceptions.crawl_exceptions import *

# FIXME remover o "mock" de localizar a palavra
def spider(url, word, maxPages):
   '''
   Este método é o principal deste módulo e "visita" url a url até atingir os limites estabelecidos.
   '''

   visitedPages = []
   pagesToVisit = [url]
   numberVisited = 0
   foundWord = False

   while numberVisited < maxPages and pagesToVisit != [] and not foundWord:
      url = pagesToVisit[0]
      pagesToVisit = pagesToVisit[1:]

      if url in visitedPages:
         print(numberVisited, 'Visitado!', url)
         # pass
      else:
         numberVisited = numberVisited + 1

         try:
            print(numberVisited, "Visiting: ", url)
            
            visitedPages = visitedPages + [url]
            
            parser = CrawlUrl(url)
            page = parser.makeTheSoup()

            data = page.text
            links = page.links

            if data.find(word) > -1:
               foundWord = True

            pagesToVisit = pagesToVisit + links
            print('*** Sucesso! ***')
         except MakeTheSoupError as mse:
            print("*** Falha! Não foi possível realizar o parse da url '%s'" % url)
         except KeyboardInterrupt:
            print("*** Falha! Crawl finalizado pelo usuário! ***")
            break
         except:
            # print('*** Falhou! ***')
            traceback.print_exc()

   if foundWord:
      result = 'A palavra ' + word + ' foi encontrada em ' + url
      print(result)
      return result
   else:
      result = 'A palavra não foi encontrada!'
      print(result)
      return result

