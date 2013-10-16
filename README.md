MR. CRAWLER
================================

O _MR. CRAWLER_ é um projeto desenvolvido na disciplina de Projetos Interativos (PI) do 4o Período do curso de Bacharelado de Ciências da Computação do Senac-SP.

**Status do projeto:** _implementação das rotinas de análise_

Escopo
----------------------
O Mr. Crawler irá capturar todos os _tweets_ em tempo real (_stream_) ou da base histórica (_search_) que satisfaçam um determinado termo fornecido.
Para realizar a coleta e análise é necessário que o usuário tenha uma conta ativa do _Twitter_, com a qual ele deverá autorizar o Mr. Crawler acessar sua conta.

Após a captura serão exibidos resultados derivados das diferentes análises realizadas:

* Frequencia de palavras;
* Diversidade léxica;
* Entidades mais frequentes;
* Diversidade e frequencia da origem dos tweets;
* Top usuários mais influentes (mais seguidores, menos interatividade);
* Top usuários mais ativos (menos seguidores, mais interatividade);
* Proporção entre tweets geolocalizados e os não-geolocalizados;

Planejados e desejáveis:

* Mapa de tweets geolocalizados;
* Relacionamentos entre os participantes;
* Tweets com maior número de retweets;

Rodando o Mr. Crawler
----------------------

Faça um clone do Mr. Crawler:

```
git clone https://github.com/eryckson/MrCrawler.git
```

Para rodar o Mr. Crawler localmente é necessário ter o Python na versão 3.3.2 e também os seguintes frameworks:

```
pip install Flask Jinja2 SQLAlchemy beautifulsoup4 html5lib lxml requests simplejson tornado twitter
```

Depois precisamos iniciar a aplicação:

```
python MrCrawler.py --logging=debug
```

e ele estará respondendo em

```
http://localhost:8080
```

Para aprender Python
----------------------
* [Python Para Zumbis - em português](http://pycursos.com/python-para-zumbis/)
* [Pythonmonk](http://pythonmonk.com)
* [Learn Python](http://docs.python-guide.org/en/latest/intro/learning/)
* [Learn Python The Hard Way](http://learnpythonthehardway.org/book/)
* [Interactive Python tutorial](http://www.learnpython.org)

----------------------

> SE EM TUDO O MAIS FOREM IDÊNTICAS AS VÁRIAS EXPLICAÇÕES DE UM FENÔMENO, A MAIS SIMPLES É A MELHOR" — WILLIAM DE OCKHAM

----------------------

Autores do projeto: [Hamilton Santana] [1],
[Ivan Probst] [2], [Lucas Ribeiro] [3] e [Eryckson Magno] [4].

  [1]: https://github.com/HamiltonSantana "hamilton@github"
  [2]: https://github.com/20ivan "ivan@github"
  [3]: https://github.com/Lux-Celeste "lucas@github"
  [4]: https://github.com/eryckson "eryckson@github"
