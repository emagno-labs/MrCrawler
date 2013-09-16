MR. CRAWLER
================================

O _MR. CRAWLER_ é um projeto desenvolvido na disciplina de Projetos Interativos (PI) do 4o Período do curso de Bacharelado de Ciências da Computação do Senac-SP.

**Status do projeto:** _estruturação do projeto e definição de escopo_

Planos e ideias
----------------------

* Captura e coleta de dados de um dado web site;
* Respeito pelo arquivo *Robots.txt*;
* Extrair e armazenar links, *forms* e emails (bem como todo o conteúdo do site, tabulando por tags);
* Análise de comentários no HTML (classificação de potenciais informações sensíveis);
* Análise de *meta tags*;
* Classificação da linguagem/tecnologia utilizada no web site;
* Tabulação dos métodos HTTP permitidos; 
* Indexação de documentos PDF e imagens e possibilidade de extração de metadados;
* Auditoria contra *sql injection*;
* Auditoria contra *xss (cross site scripting)*;
* Auditoria contra *csrf (cross site request forgery)*;
* Busca e interpretação de *site maps* para aumentar a superfície de análise;
* E mais: *cross domain js*, *code disclosure*, *blank body*, *dot net event validation*, *http in body*...

Rodando o Mr. Crawler
----------------------

Faça um clone do Mr. Crawler:

```
git clone https://github.com/eryckson/MrCrawler.git
```

Para rodar o Mr. Crawler localmente é necessário ter o Python na versão 3.3.2 e também os seguintes frameworks:

```
pip install Flask
pip install tornado
pip install beautifulsoup4
pip install html5lib
pip install lxml
```

Depois basta:

```
python MrCrawler.py --logging=debug
```

e ele estará respondendo em

```
http://localhost:8080
```

Mais em Python
----------------------
* [Learn Python](http://docs.python-guide.org/en/latest/intro/learning/)

----------------------

> SE EM TUDO O MAIS FOREM IDÊNTICAS AS VÁRIAS EXPLICAÇÕES DE UM FENÔMENO, A MAIS SIMPLES É A MELHOR" — WILLIAM DE OCKHAM

----------------------

Autores do projeto: [Hamilton Santana] [1],
[Ivan Probst] [2], [Lucas Ribeiro] [3] e [Eryckson Magno] [4].

  [1]: https://github.com/HamiltonSantana "hamilton@github"
  [2]: https://github.com/20ivan "ivan@github"
  [3]: https://github.com/Lux-Celeste "lucas@github"
  [4]: https://github.com/eryckson "eryckson@github"
