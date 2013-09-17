import re
from lxml import etree

# TODO importar o módulo de persistencia para armazenar em banco de dados a análise e os resultados
# FIXME nao seria legal utilizar o bs4 para o tratamento do DOM e o lxml para o parser?

class ajax(object):

   def __init__(self):
      # TODO verificar se uma URL já foi analisada a partir da base de dados
      # self._already_inspected = [];

      # criando a expressao regular para a busca por codigo ajax
      ajax_regex_string = '(XMLHttpRequest|eval\(|ActiveXObject|Msxml2\.XMLHTTP|'
      ajax_regex_string += 'ActiveXObject|Microsoft\.XMLHTTP)'
      self._ajax_regex_re = re.compile(ajax_regex_string, re.IGNORECASE)

      # compilando o XPATH
      self._script_xpath = etree.XPath('.//script')

   def grep(self, request, response):
      url = response.get_url()
  
      if response.is_text_or_html(): # and url not in self._already_inspected:

         # TODO armazenar a url como já analisada em base de dados
         # self._already_inspected.add(url)

         dom = response.get_dom()
         
         # In some strange cases, we fail to normalize the document
         if dom is None:
            return
            
         script_elements = self._script_xpath(dom)
         
         for element in script_elements:
            # returns the text between <script> and </script>
            script_content = element.text

            if script_content is not None:

               res = self._ajax_regex_re.search(script_content)
               
               if res:
                  desc = 'The URL: "%s" has AJAX code.' % url

                  # TODO armazenar o resultado em banco de dados (não em formato de log... tabulado é melhor!) =]
                  # i = Info('AJAX code', desc, response.id, self.get_name())
                  # i.set_url(url)
                  # i.add_to_highlight(res.group(0))
                        
                  # self.kb_append_uniq(self, 'ajax', i, 'URL')
