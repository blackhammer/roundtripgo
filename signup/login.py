#!/usr/bin/env python

import webapp2
import re
import hashlib
import random
import string

from google.appengine.ext import db
from usermanager import *

from mako.template import Template

import sys
import os
sys.path.append("../db") 
sys.path.append("../mako")
sys.path.append("../markupsafe") 


class LoginHandler(webapp2.RequestHandler):
	def get(self):
		self.write_form()
		
	def post(self):
		username	= self.request.get('username')
		passwd 	= self.request.get('password')
		
		user = self.get_user(username)
		
		if user:
			passhash = self.validate_passwd(user.UserName, passwd, user.Salt)
			if passhash == user.Password:				
				usercookie = '%d|%s' % (user.key().id(),hashlib.sha256(user.UserName + user.Salt).hexdigest())
				self.response.headers.add_header('Set-Cookie', 'user_id=%s; Path=/'% usercookie) 
				self.redirect("/home")
		
		self.write_form(username,"Invalid login")
		
	def validate_passwd(self,username, password, salt):    
	  h = hashlib.sha256(username + password + salt).hexdigest()
	  return '%s,%s' % (h, salt)	  
	  
	def get_user(self, username):
		query = "SELECT * FROM User WHERE UserName = '%s'" % username
		users = db.GqlQuery(query)
		
		if users.count() == 1:
			return users[0]
		else:
			return None
		
	def write_form(self,user="",userloginerror=""):
		path = os.path.join(os.path.dirname(__file__), '../pages/login.html')
		template = Template(filename=path)
		response = template.render(username=user,loginerror=userloginerror)
		self.response.out.write(response)
		
		
class LogoutHandler(webapp2.RequestHandler):
	def get(self):
		self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/') 
		self.redirect("/")
	def post(self):
		pass		

		