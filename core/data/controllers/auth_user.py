'''
Este módulo é responsável pelas funcionalidades de autenticação e autorização de um usuário, bem como de seu registro/manutenção.
'''

from core.data.orm.database import db_session
from core.data.orm.models import User
import re

def register_user(login, name, email, pwd, pwd_confirmation):
   '''
   Este método é responsável por validar e registrar um novo usuário.

   :return: Um booleano indicando se houve sucesso e uma string contendo a mensagem
   '''

   try:
      if login is None or login == '':
         return False, 'O login é obrigatório'
      
      if name is None or name == '':
         return False, 'O nome é obrigatório'

      if email is None or email == '':
         return False, 'O e-mail é obrigatório'
      else:
         # TODO validar se o email informado está em um formato válido
         pass

      if pwd is None or pwd == '' or pwd_confirmation is None or pwd_confirmation == '':
         return False, 'A senha e sua confirmação devem ser informadas'
   
      if pwd != pwd_confirmation:
         return False, 'A senha não confere com sua confirmação'
   
      if name in pwd:
         return False, 'A senha não deve conter o nome do usuário'

      if login in pwd:
         return False, 'A senha não deve conter o login do usuário'

      if email in pwd:
         return False, 'A senha não deve conter o email do usuário'
      
      if len(pwd) < 6:
         return False, 'A senha deve possuir ao menos 6 caracteres'
      
      # aplicando as expressões regulares
      p = re.compile('[A-Z]+')
      m = p.match(pwd)

      if m is None:
         return False, 'A senha deve possuir ao menos uma letra maiúscula'

      p = re.compile('[a-z]+')
      m = p.match(pwd)

      if m is None:
         return False, 'A senha deve possuir ao menos uma letra minúscula'

      p = re.compile('\d+')
      m = p.match(pwd)

      if m is None:
         return False, 'A senha deve possuir ao menos um número'
   
      # TODO implementar verificação se a senha possui ao menos um caracter especial

      # FIXME cifrar a senha, no mínimo SHA-256 "com sal"
      user = User(login, name, email, pwd)
      db_session.add(u)
      db_session.commit()
   
      return True, 'O usuário "%s" foi criado com sucesso!' % name

   except:
      return False, 'Não foi possível criar o usuário "%s"' % name

