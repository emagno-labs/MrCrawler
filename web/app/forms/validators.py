'''
Este módulo implementa validações a serem utilizadas pelos formulários web
'''

import re
from wtforms.validators import ValidationError
from core.data.orm.models import User

def isEmail(form, field):
   '''
   Este método verifica se o dado informado representa um email com formato [básico]  válido.
   '''

   email = field.data

   if email:
      if not re.match(r"^[a-zA-Z0-9._%-]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}$", email):
         raise ValidationError("O e-mail informado é inválido.")

def isEmailUsed(form, field):
   '''
   Este método verifica se um email informado já está em uso para um usuário.
   '''

   email = field.data

   if email:
      u = User.query.filter(User.email == email).first()
      if u is not None:
         raise ValidationError('O e-mail informado já está em uso.')

def isStrongPassword(form, field):
   '''
   Este método verifica se uma senha informada está "forte" o suficiente.
   '''

   login = field.data

   if login:
      if len(re.findall(r"[A-Z]", login)) <= 0:
         raise ValidationError('A senha deve possuir ao menos uma letra maiúscula.')

      if len(re.findall(r'[a-z]+', login)) <= 0:
         raise ValidationError('A senha deve possuir ao menos uma letra minúscula.')

      if len(re.findall(r'\d+', login)) <= 0:
         raise ValidationError('A senha deve possuir ao menos um número.')

def isUnusedLogin(form, field):
   '''
   Este método verifica se um login informado já está em uso por um usuário.
   '''

   login = field.data

   if login:
      u = User.query.filter(User.login == login).first()
      if u is not None:
         raise ValidationError('O login escolhido já está em uso')
