#!/bin/python3.3.2
# -`*- coding: utf-8 -*-

'''
Este módulo define e implementa os formulários web.
'''

from wtforms import Form, BooleanField, TextField, PasswordField, validators
from webapp.forms.validators import * 

class RegistrationForm(Form):
   '''
   Esta classe representa o formulário de registro de um nóvo usuário.
   '''

   login = TextField('Login', [
      validators.Length(min=4, max=25, message=('O tamanho deve ser entre %(min)d e %(max)d caracteres.')),
      isUnusedLogin
   ])
   
   name = TextField('Nome', [
      validators.Length(min=4, max=50, message=('O tamanho deve ser entre %(min)d e %(max)d caracteres.'))
   ])

   email = TextField('Email', [
      validators.Length(min=6, max=35, message=('O tamanho deve ser entre %(min)d e %(max)d caracteres.')),
      isEmail
   ])
   
   password = PasswordField('Senha', [
      validators.Required(message=('Este campo é obrigatório')),
      validators.EqualTo('confirm', message='As senhas devem ser iguais'),
      isStrongPassword
   ])
   
   confirm = PasswordField('Repita a senha')

class LoginForm(Form):
   '''
   Esta classe representa o formulário de login.
   '''

   login = TextField('Login', [
      validators.Required(message=('Informe o login'))
   ]);

   password = PasswordField('Senha', [
      validators.Required(message=('Informe a senha'))
   ])
