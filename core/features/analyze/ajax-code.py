import re
from core.controllers.crawler.mrc import Crawl

# TODO importar o módulo de persistencia para armazenar em banco de dados a análise e os resultados
# FIXME impor implementação de interface comum de analise

class AjaxCode(object):

   def __init__(self):
      # criando a expressao regular para a busca por codigo ajax (verificando jquery e mootools também)
      ajax_regex_string = '(XMLHttpRequest|eval\(|ActiveXObject|Msxml2\.XMLHTTP|ActiveXObject|Microsoft\.XMLHTTP|$.ajax|$.get|$.post|new Request\()'
      self._ajax_regex_re = re.compile(ajax_regex_string, re.IGNORECASE)

   def analyze(self, crawler):
      url = crawler._url
      
      scripts = crawler.getScripts()

      if scripts is None:
         return

      for element in scripts:

         # obtem o texto entre <script> e </script>
         script_content = element.text

         if script_content is not None:

            # aplicando expressão regular
            res = self._ajax_regex_re.search(script_content)
               
            if res:
               desc = 'A url: "%s" possui código AJAX.' % url
               # TODO armazenar o resultado em banco de dados (não em formato de log... tabulado é melhor!) =]
