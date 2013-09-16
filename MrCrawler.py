# importando móduo de manipulacao da app web
from web.app import app, server

# importando módulo de manipulacao da base de dados
from core.data.dbms import database

if __name__ == '__main__':
   # rodando a app com o Flask atuando como servidor web
   #app.run(debug=True)

   # rodando a app com o CherryPy atuando como servidor web
   try:
      server.start()
   except KeyboardInterrupt:
      server.stop()
