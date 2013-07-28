#!/usr/bin/env python

import sys
import os
import re
import hashlib
import random
import string

sys.path.append("../yellow/business")
sys.path.append("../db")
sys.path.append("../mako")
sys.path.append("../markupsafe")

from usermanager import *
import webapp2
from mako.template import Template


class HomeHandler(webapp2.RequestHandler):
	def get(self):			
		usercookie = self.request.cookies.get('user_id', '0')
		validcookie = self.validate_cookie(usercookie)
		
		if validcookie:
			userid = usercookie.split('|')[0]
			user = User.get_by_id(int(userid))
			if user:
				path = os.path.join(os.path.dirname(__file__), '../pages/index.html')
				template = Template(filename=path)
				response = template.render(username=user.UserName)
				self.response.out.write(response)
			else:
				self.redirect("/")			
		else:
			self.redirect("/login")
		
	def validate_cookie(self, cookie):
		tokens = cookie.split('|')
		if len(tokens) > 1:
			userid = tokens[0]
			cookiehash = tokens[1]
			user = User.get_by_id(int(userid))

			hash = hashlib.sha256(user.UserName + user.Salt).hexdigest()
		
			if hash == cookiehash:
				return True
			else:
				return False
		else:
			return False
	