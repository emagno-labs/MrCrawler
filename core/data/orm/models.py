#!/bin/python3.3.2
# -`*- coding: utf-8 -*-

'''
Este módulo é responsável pela definição e implementação do modelo de dados.
A partir do modo declarativo do sqlalchemy cada classe representa uma tabela no banco de dados mapeada (ORM).
'''
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean, Numeric
from core.data.orm.database import Base
from sqlalchemy.orm import relationship, backref
from datetime import datetime

class User(Base):
   '''
   Esta classe armazena os usuários autorizados pelo twitter
   '''
   __tablename__ = 'users'

   # dados de autenticação do Mr Crawler
   id = Column(Integer, primary_key=True)
   oauth_token = Column(String(50), unique=True)
   oauth_token_secret = Column(String(50), unique=True)
   created = Column(DateTime, default=datetime.now)
   last_access = Column(DateTime, default=datetime.now)
   browser = Column(String(50))
   is_temporary = Column(Boolean, default=True)

   # dados das credenciais do twitter
   id_twitter = Column(Integer)
   name = Column(String(50))
   screen_name = Column(String(50))
   description = Column(Text)
   lang = Column(String(10))
   time_zone = Column(String(50))
   location = Column(String(100))
   geo_enabled = Column(Boolean, default=False)
   url = Column(String(100))
   profile_image_url = Column(String(250))
   friends_count = Column(Integer)
   statuses_count = Column(Integer)
   favourites_count = Column(Integer)

   def __init__(self, oauth_token=None, oauth_token_secret=None, name=None, browser=None):
      self.oauth_token = oauth_token
      self.oauth_token_secret = oauth_token_secret
      self.name = name
      self.browser = browser

   def __repr__(self):
      return '<User %r>' % (self.name)

class TweetFindOut(Base):
   '''
   Esta classe define a pesquisas/procuras por tweets realizadas
   '''
   __tablename__ = 'tweets_find_out'

   id = Column(Integer, primary_key=True)
   term = Column(String(100))
   search_type = Column(String(30))
   max_tweets = Column(Integer)
   created = Column(DateTime, default=datetime.now)

   # foreign keys
   user_id = Column(Integer, ForeignKey('users.id'))

   # many-to-one relationships
   user = relationship("User", backref=backref('tweets_find_out', order_by=id))

   def __init__(self, term=None, search_type=None, max_tweets=1000, user_id=None):
      self.term = term
      self.search_type = search_type
      self.max_tweets = max_tweets
      self.user_id = user_id

class Tweet(Base):
   '''
   Esta classe armazena os tweets coletados (a partir de uma definição em "TweetFindOut")
   '''
   __tablename__ = 'tweets'

   id = Column(Integer, primary_key=True)
   text = Column(Text)
   captured = Column(DateTime, default=datetime.now)
   created_at = Column(DateTime)
   source = Column(String(50))
   lat = Column(Numeric(precision=15, scale=8))
   lng = Column(Numeric(precision=15, scale=8))
   user_name = Column(String(50))
   user_id = Column(Integer)
   user_description = Column(String(200))
   user_created_at = Column(DateTime)
   user_followers_count = Column(Integer)
   user_friends_count = Column(Integer)
   user_profile_image_url = Column(String(300))
   tweet = Column(Text)

   # foreign Keys
   tweet_find_out_id = Column(Integer, ForeignKey("tweets_find_out.id"))

   # many-to-one relationships
   tweet_find_out = relationship("TweetFindOut", backref=backref("tweets", order_by=id))

# class Analyze(Base):
#    '''
#    Esta classe armazena as análises realizadas sobre uma pesquisa (TweetFindOut)
#    '''
#    __tablename__ = 'analyzes'

#    id = Column(Integer, primary_key=True)
#    term = Column(String(100))
#    search_type = Column(String(30))
#    max_tweets = Column(Integer)
#    created = Column(DateTime, default=datetime.now)

#    # foreign Keys
#    tweet_find_out_id = Column(Integer, ForeignKey("tweets_find_out.id"))

#    # many-to-one relationships
#    tweet_find_out = relationship("TweetFindOut", backref=backref("analyzes", order_by=id))

# class Page(Base):
#    '''
#    Esta classe define uma página que foi analisada.
#    Uma página pode possuir links (outras páginas) poderão também ser analisados.
#    '''

#    __tablename__ = 'pages'

#    id = Column(Integer, primary_key=True)
#    url = Column(String(250))
#    created = Column(DateTime, default=datetime.now)
#    markup = Column(Text)
#    text = Column(Text)

#    # foreign Keys
#    analyze_id = Column(Integer, ForeignKey("analyzes.id"))
#    parent_page_id = Column(Integer, ForeignKey('pages.id'))

#    # many-to-one relationships
#    analyze = relationship("Analyze", backref=backref("pages", order_by=id))

#    # one-to-many relationships
#    pages = relationship("Page", backref=backref('parent_page', remote_side=[id]))

#    def __init__(self, url=None, markup=None, text=None):
#       self.url = url
#       self.markup = markup
#       sefl.text = text

#    def __repr__(self):
#       return '<Page %r>' % (self.url)

# class Script(Base):
#    '''
#    Esta classe define um script (tag script) encontrada em uma página.
#    '''

#    __tablename__ = 'scripts'

#    id = Column(Integer, primary_key=True)
#    source = Column(String(250))
#    type = Column(String(30))
#    code = Column(Text)

#    # foreign keys
#    page_id = Column(Integer, ForeignKey('pages.id'))

#    # many-to-one relationships
#    page = relationship("Page", backref=backref('scripts', order_by=id))

# class Comment(Base):
#    '''
#    Esta classe define um comentário encontrado em uma página.
#    '''

#    __tablename__ = 'comments'

#    id = Column(Integer, primary_key=True)
#    text = Column(Text)

#    # foreign keys
#    page_id = Column(Integer, ForeignKey('pages.id'))

#    # many-to-one relationships
#    page = relationship("Page", backref=backref('comments', order_by=id))

# class Vulnerability(Base):
#    '''
#    Esta classe define as diferentes vulnerabilidades que uma página (e seus componentes) podem possuir.
#    '''

#    __tablename__ = 'vulnerabilities'

#    id = Column(Integer, primary_key=True)
#    name = Column(String(100))
#    description = Column(Text)

# class PageVulnerability(Base):
#    '''
#    Esta classe define as vulnerabilidades que foram localizadas em uma página analisada.
#    '''

#    __tablename__ = 'page_vulnerabilities'

#    id = Column(Integer, primary_key=True)
#    created = Column(DateTime, default=datetime.now)
#    is_critical = Column(Boolean)
#    text = Column(Text)

#    # foreign keys
#    page_id = Column(Integer, ForeignKey('pages.id'))
#    vuln_id = Column(Integer, ForeignKey('vulnerabilities.id'))

#    # many-to-one relationships
#    page = relationship('Page', backref=backref('pageanalyzes', order_by=id))
#    vuln = relationship('Vulnerability', backref=backref('pageanalyzes', order_by=id))

