from urllib import parse
from urllib.request import urlopen
from bs4 import BeautifulSoup

class MrCrawler():

   def getLinks(self, url):
      try:
         self.links = []
         self.baseUrl = url
         response = urlopen(url)
         soup = BeautifulSoup(response.read(), "lxml")

         for l in soup.find_all('a'):
            value = l.get('href')
            newUrl = parse.urljoin(self.baseUrl, value)
            self.links = self.links + [newUrl]

         return soup.get_text(), self.links
      except:
         return "", []

def spider(url, word, maxPages):
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
            parser = MrCrawler()
            data, links = parser.getLinks(url)
            visitedPages = visitedPages + [url]

            if data.find(word) > -1:
               foundWord = True

            pagesToVisit = pagesToVisit + links
            print('*** Sucesso! ***')
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

