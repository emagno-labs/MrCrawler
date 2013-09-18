import re
from lxml import etree
from core.controllers.crawler.mrc import Crawl

# TODO importar o módulo de persistencia para armazenar em banco de dados a análise e os resultados
# FIXME impor implementação de interface comum de analise

class AjaxCode(object):

   def __init__(self):
      # TODO verificar se uma URL já foi analisada a partir da base de dados
      # self._already_inspected = [];

      # criando a expressao regular para a busca por codigo ajax
      # FIXME adicionar análise de código ajax de bibliotecas como o jquery
      ajax_regex_string = '(XMLHttpRequest|eval\(|ActiveXObject|Msxml2\.XMLHTTP|ActiveXObject|Microsoft\.XMLHTTP)'
      self._ajax_regex_re = re.compile(ajax_regex_string, re.IGNORECASE)

   def analyze(self, crawler):
      url = crawler._url
      
      scripts = crawler.getScripts()

      if scripts: # and url not in self._already_inspected:

         # TODO armazenar a url como já analisada em base de dados
         # self._already_inspected.add(url)

         for element in scripts:

            # obtem o texto entre <script> e </script>
            script_content = element.text

            if script_content is not None:

               # aplicando expressão regular
               res = self._ajax_regex_re.search(script_content)
               
               if res:
                  desc = 'A url: "%s" possui código AJAX.' % url

                  # TODO armazenar o resultado em banco de dados (não em formato de log... tabulado é melhor!) =]
                  # i = Info('AJAX code', desc, response.id, self.get_name())
                  # i.set_url(url)
                  # i.add_to_highlight(res.group(0))
                        
                  # self.kb_append_uniq(self, 'ajax', i, 'URL')
