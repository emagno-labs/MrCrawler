'''
Este módulo é responsável por criar e manutenir a base de dados, bem como fornecer uma sessão para a manipulação dos dados.
'''

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# cria a engine do banco de dados
engine = create_engine('sqlite:///core/data/db/mrcrawler.db', convert_unicode=True)

# cria uma sessão para manipulação dos dados
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

# inicia a base declarativa para os dados
Base = declarative_base()
Base.query = db_session.query_property()

def init():
   '''
   Este método importa os modelos e cria toda a base de dados
   '''

   import core.data.orm.models
   Base.metadata.create_all(bind=engine)

def backup():
   # TODO implementar rotina de backup da base de dados (desejável salvar na nuvem)
   pass

def reset():
   # TODO implementar rotina de limpeza de toda a base (pode ser remover o arquivo .db)
   pass
