from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from core.data.orm.database import Base
from sqlalchemy.orm import relationship, backref

from datetime import datetime

class User(Base):
   __tablename__ = 'users'
   
   id = Column(Integer, primary_key=True)
   login = Column(String(20), unique=True)
   name = Column(String(50), unique=True)
   email = Column(String(120), unique=True)
   created = Column(DateTime, default=datetime.now)
   pwd = Column(String(200))

   def __init__(self, name=None, email=None, pwd=None):
      self.name = name
      self.email = email
      self.pwd = pwd

   def __repr__(self):
      return '<User %r>' % (self.name)

class Analyze(Base):
   __tablename__ = 'analyzes'

   id = Column(Integer, primary_key=True)
   target_url = (String(250))
   created = Column(DateTime, default=datetime.now)

   # foreign keys
   user_id = Column(Integer, ForeignKey('users.id'))

   # many-to-one relationships
   user = relationship("User", backref=backref('analyzes', order_by=id))

class Page(Base):
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
   __tablename__ = 'comments'

   id = Column(Integer, primary_key=True)
   text = Column(Text)
   
   # foreign keys
   page_id = Column(Integer, ForeignKey('pages.id'))

   # many-to-one relationships
   page = relationship("Page", backref=backref('comments', order_by=id))
