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
   Esta classe define um usuário do sistema
   '''

   __tablename__ = 'users'
   
   id = Column(Integer, primary_key=True)
   login = Column(String(20), unique=True)
   name = Column(String(50), unique=True)
   email = Column(String(120), unique=True)
   created = Column(DateTime, default=datetime.now)
   pwd = Column(String(200))

   def __init__(self, login=None, name=None, email=None, pwd=None):
      self.login = login
      self.name = name
      self.email = email
      self.pwd = pwd

   def __repr__(self):
      return '<User %r>' % (self.name)

class Tweet(Base):
   '''
   Esta classe armazena os tweets coletados
   '''

   __tablename__ = 'tweets'

   id = Column(Integer, primary_key=True)
   term = Column(String(200))
   text = Column(Text)
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

class Analyze(Base):
   '''
   Esta classe define uma análise a uma url alvo (target_url).
   Um usuário realiza uma análise que pode ter várias páginas analisadas.
   '''

   __tablename__ = 'analyzes'

   id = Column(Integer, primary_key=True)
   target_url = (String(250))
   created = Column(DateTime, default=datetime.now)

   # foreign keys
   user_id = Column(Integer, ForeignKey('users.id'))

   # many-to-one relationships
   user = relationship("User", backref=backref('analyzes', order_by=id))

class Page(Base):
   '''
   Esta classe define uma página que foi analisada.
   Uma página pode possuir links (outras páginas) poderão também ser analisados.
   '''

   __tablename__ = 'pages'

   id = Column(Integer, primary_key=True)
   url = Column(String(250))
   created = Column(DateTime, default=datetime.now)
   markup = Column(Text)
   text = Column(Text)
   
   # foreign Keys
   analyze_id = Column(Integer, ForeignKey("analyzes.id"))
   parent_page_id = Column(Integer, ForeignKey('pages.id'))
   
   # many-to-one relationships
   analyze = relationship("Analyze", backref=backref("pages", order_by=id))

   # one-to-many relationships
   pages = relationship("Page", backref=backref('parent_page', remote_side=[id]))

   def __init__(self, url=None, markup=None, text=None):
      self.url = url
      self.markup = markup
      sefl.text = text

   def __repr__(self):
      return '<Page %r>' % (self.url)

class Script(Base):
   '''
   Esta classe define um script (tag script) encontrada em uma página.
   '''

   __tablename__ = 'scripts'

   id = Column(Integer, primary_key=True)
   source = Column(String(250))
   type = Column(String(30))
   code = Column(Text)

   # foreign keys
   page_id = Column(Integer, ForeignKey('pages.id'))

   # many-to-one relationships
   page = relationship("Page", backref=backref('scripts', order_by=id)) 

class Comment(Base):
   '''
   Esta classe define um comentário encontrado em uma página.
   '''

   __tablename__ = 'comments'

   id = Column(Integer, primary_key=True)
   text = Column(Text)
   
   # foreign keys
   page_id = Column(Integer, ForeignKey('pages.id'))

   # many-to-one relationships
   page = relationship("Page", backref=backref('comments', order_by=id))

class Vulnerability(Base):
   '''
   Esta classe define as diferentes vulnerabilidades que uma página (e seus componentes) podem possuir.
   '''

   __tablename__ = 'vulnerabilities'

   id = Column(Integer, primary_key=True)
   name = Column(String(100))
   description = Column(Text)

class PageVulnerability(Base):
   '''
   Esta classe define as vulnerabilidades que foram localizadas em uma página analisada.
   '''

   __tablename__ = 'page_vulnerabilities'

   id = Column(Integer, primary_key=True)
   created = Column(DateTime, default=datetime.now)
   is_critical = Column(Boolean)
   text = Column(Text)
   
   # foreign keys
   page_id = Column(Integer, ForeignKey('pages.id'))
   vuln_id = Column(Integer, ForeignKey('vulnerabilities.id'))

   # many-to-one relationships
   page = relationship('Page', backref=backref('pageanalyzes', order_by=id))
   vuln = relationship('Vulnerability', backref=backref('pageanalyzes', order_by=id))

