import sqlite3
from contextlib import closing

# conexao com o banco
def connect_db(database):
   try:
      return sqlite3.connect(database)
   except:
      pass
      # raise # TODO como disparar uma excecao?

# CUIDADO! este método cria ou recria toda a base! se existirem dados os mesmos serão perdidos!
def init_db(schema):
   if schema is None:
      pass
      # TODO como disparar uma excecao?
   
   try:
      with closing(connect_db()) as db:
         with app.open_resource(schema, mode='r') as f:
            db.cursor().executescript(f.read())
         db.commit()
   except:
      pass
      # TODO como disparar uma excecao?

# metodo responsavel pela geração de um backup da base de dados
def backup_db():
   pass
