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
sys.path.append("./mako")
sys.path.append("./markupsafe") 

class SignUpHandler(webapp2.RequestHandler):
	USER_RE 		= re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
	PASSWD_RE 	= re.compile(r"^.{3,20}$")
	EMAIL_RE 	= re.compile(r"^[\S]+@[\S]+\.[\S]+$")
	
	def write_form(self,user="",usernameerror="",passerror="",passmatcherror="",useremail="",useremailerror=""):
		
		path = os.path.join(os.path.dirname(__file__), '../pages/signup.html')
		template = Template(filename=path)
		response = template.render(username=user,usererror=usernameerror,pwerror=passerror,pwmatcherror=passmatcherror, email=useremail, \
		emailerror=useremailerror)
		self.response.out.write(response)
		
	
	def get(self):
		self.write_form()
	
	def post(self):
		#Get params
		user 		= self.request.get('username')
		passwd 	= self.request.get('password')
		verify 	= self.request.get('verify')
		email 	= self.request.get('email')
		
		#validate
		usermatch	= self.validate_user(user)
		passwdmatch	= self.validate_passwd(passwd)
		verifymatch	= self.validate_passwd_match(passwd, verify)
		emailmatch  = self.validate_email(email)
		userexists  = self.user_exists(user)
			
		if usermatch and passwdmatch and verifymatch and emailmatch and not userexists:
			id = self.addUser(user, passwd, email)
			self.redirectToWelcome(user, id)
			
		
		usererror = ""
		emailerror = ""
		passwderr = ""
		passwdmatcherr = ""		
		
		if usermatch is None:
			usererror = "That is not a valid username"
		if passwdmatch is None:
			passwderr = "That is not a valid password"
		if verifymatch is None:
			passwdmatcherr = "Those passwords do not match"
		if emailmatch is None:
			emailerror = "That is not a valid email address"
		if userexists is True:
			usererror = "That user already exists" 
			
		self.write_form(user, usererror,passwderr,passwdmatcherr,email,emailerror)		
	
	def user_exists(self, username):
		query = "SELECT * FROM User WHERE UserName = '%s'" % username
		users = db.GqlQuery(query)
		
		if users.count() > 0:
			return True
		else:
			return False

	def addUser(self, user, password, email):
		salt = self.make_salt()
		passwd = self.secure_password(user, password, salt)
		newuser = User(UserName = user, Password = passwd, Salt = salt, Email = email)
		newuser.put()
		return newuser.key().id()
		
	def secure_password(self,username, password, salt):    
	  h = hashlib.sha256(username + password + salt).hexdigest()
	  return '%s,%s' % (h, salt)
		
	def make_salt(self):
		return ''.join(random.choice(string.letters) for x in xrange(5))
		
	def redirectToWelcome(self, username, id):
		#create a cookie and hash it
		user = User.get_by_id(int(id))
		usercookie = '%d|%s' % (id,hashlib.sha256(user.UserName + user.Salt).hexdigest())
		
		self.response.headers.add_header('Set-Cookie', 'user_id=%s; Path=/'% usercookie) 
		
		self.redirect("/")
		
	def validate_user(self, username):
		return self.USER_RE.match(username)
		
	def validate_passwd(self, passwd):
		if passwd == "":
			return None
		return self.PASSWD_RE.match(passwd)
		
	def validate_email(self, email):
		if email == "":
			return "verified" #return something other than empty string to show empty email is accepted
		return self.EMAIL_RE.match(email)
							
	def validate_passwd_match(self, passwd, verify):
		if passwd == verify:
			return verify
		else:
			return None	

